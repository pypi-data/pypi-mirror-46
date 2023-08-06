import acrawler
from typing import List, Dict
import asyncio
import logging
import time
import traceback
import signal
import pickle
from pathlib import Path


from acrawler.task import Task, SpecialTask
from acrawler.http import Request
from acrawler.scheduler import Scheduler, RedisDupefilter, RedisPQ
from acrawler.middleware import middleware
from acrawler.utils import merge_config, config_from_setting, to_asyncgen
from acrawler.item import DefaultItem
import acrawler.setting as DEFAULT_SETTING
from importlib import import_module
from pprint import pformat

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

# typing
from typing import Tuple, Dict, Any, Type, TYPE_CHECKING
import acrawler
_Config = Dict[str, Any]
_Response = acrawler.http.Response


logger = logging.getLogger(__name__)


class Worker:
    """Worker execute the task.

    One :class:`Crawler` will create many workers. A worker will
    - calls its scheduler's methods
    - implements task's retry mechanism
    - catch the result of a task's execution
    """

    def __init__(self, crawler: 'Crawler', sdl: Scheduler = None, ):
        self.crawler = crawler
        self.sdl = sdl or Scheduler()
        self._max_tries = self.crawler.max_tries
        self.current_task = None

    async def work(self):
        try:
            while True:
                self.current_task = await self.sdl.consume()
                task = self.current_task
                exception = False
                try:
                    added = False
                    async for new_task in task.execute():
                        if isinstance(new_task, Exception):
                            raise new_task
                        added = await self.crawler.add_task(new_task)
                except asyncio.CancelledError as e:
                    raise e
                except Exception as e:
                    logger.error('{} execution faces {}'.format(task, e))
                    logger.error(traceback.format_exc())
                    exception = True

                retry = False
                if exception:
                    logger.warning(
                        'Task failed %s for %d times.', task, task.tries)
                    if task.tries < self._max_tries:
                        task.dont_filter = True
                        await self.sdl.produce(task)
                        retry = True
                        self.crawler.counter.task_add()
                    else:
                        logger.warning(
                            'Drop the task %s', task)
                    self.crawler.counter.task_done(task, 0)
                else:
                    self.crawler.counter.task_done(task, 1)

                if task.recrawl > 0 and not retry:
                    task.tries = 0
                    task.init_time = time.time()
                    task.exetime = task.last_crawl_time + task.recrawl
                    task.dont_filter = True
                    await self.crawler.add_task(task)

                self.current_task = None
        except asyncio.CancelledError as e:
            if self.current_task:
                self.current_task.tries -= 1
                task.dont_filter = True
                logger.info('During shutdown, put back {}'.format(task))
                await self.sdl.produce(task)
            raise e
        except Exception as e:
            logger.error(traceback.format_exc())


class Counter:
    """A global counter records unfinished count of tasks.
    """

    def __init__(self, loop=None):
        self.counts = {}
        self._unfinished_tasks = 0
        self._finished = asyncio.Event(loop=loop)
        self._finished.set()
        self.always_lock = False

    def lock_always(self):
        self._finished.clear()
        self.always_lock = True

    async def join(self):
        if self.always_lock:
            await self._finished.wait()
        else:
            if self._unfinished_tasks > 0:
                await self._finished.wait()

    def task_add(self):
        self._unfinished_tasks += 1
        self._finished.clear()

    def task_done(self, task, success: int = 1):
        for family in task.families:
            rc = self.counts.setdefault(family, [0, 0])
            rc[success] += 1
        if self.always_lock:
            self._unfinished_tasks -= 1
        else:
            if self._unfinished_tasks <= 0:
                raise ValueError('task_done() called too many times')
            self._unfinished_tasks -= 1
            if self._unfinished_tasks == 0:
                self._finished.set()

    def __getstate__(self):
        state = self.__dict__
        state.pop('_finished', None)
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.__dict__['_finished'] = asyncio.Event()
        self.__dict__['_finished'].set()

class Crawler(object):
    """This is the base crawler, from which all crawlers that you write yourself must inherit.

    Attributes:

    """

    max_tries: int = 3
    """A task will try to execute for `max_tries` times before complete fail."""

    max_requests: int = 5
    """A crawler will obtain `max_requests` request concurrently."""

    start_urls: List[str] = []
    """Ready for vanilla :meth:`start_requests`"""

    parsers: List['acrawler.Parser'] = []
    """Shortcuts for parsing response. 

    Crawler will automatically append :meth:`acrawler.parser.Parser.parse` to response's 
    callbacks list for each parser in parsers.
    """

    request_config: _Config = {}
    """Key-Value pairs will be passed as keyword arguments to every sended `aiohttp.request`.

    acceptable keyword
        params - Dictionary or bytes to be sent in the query string of the new request

        data - Dictionary, bytes, or file-like object to send in the body of the request

        json - Any json compatible python object

        headers - Dictionary of HTTP Headers to send with the request

        cookies - Dict object to send with the request

        allow_redirects - If set to False, do not follow redirects

        timeout - Optional ClientTimeout settings structure, 5min total timeout by default.
    """

    middleware_config: _Config = {}
    """Key-value pairs for handler-priority.

    Examples:
        Handler with higer priority handles the task earlier. Priority 0 will disable the handler::

            {
                'some_old_handler': 0,
                'myhandler_first': 1000,
                'myhandler': 500
            }

    """

    config: _Config = {}
    """Config dictionary for this crawler. See avaliable options in `setting`.
    """



    def __init__(self):

        self.loop = asyncio.get_event_loop()
        if not hasattr(self, 'max_workers'):
            self.max_workers = self.max_requests

        self._form_config()
        self._logging_config()

        self.counter: Counter = None
        self.shedulers: Dict[str, 'Scheduler'] = {}
        self._create_schedulers()
        self.workers: List['Worker'] = []

        self.middleware = middleware
        """Singleton object :class:`acrawler.middleware.middleware`"""

        self.middleware.crawler = self
        self._add_default_middleware_handler_cls()
        logger.info("Initializing middleware's handlers...")
        logger.info(self.middleware)

    def run(self):
        """Core method of the crawler. Usually called to start crawling."""

        signals = (signal.SIGINT, )
        for s in signals:
            self.loop.add_signal_handler(
                s, lambda s=s: self.loop.create_task(self.ashutdown(s)))

        self.run_task = self.loop.create_task(self.arun())
        self.loop.run_forever()

    async def arun(self):
        # Wraps main works and wait until all tasks finish.
        try:
            logger.info("Start crawling...")
            await self._on_start()
            await CrawlerStart(self).execute()
            await self.manager()

            await CrawlerFinish(self).execute()
            await self.ashutdown()
        except asyncio.CancelledError:
            pass
        except Exception:
            logger.error(traceback.format_exc())

    async def manager(self):
        """Create multiple workers to execute tasks.
        """
        try:
            self.loop.create_task(self._log_status_timer())
            for _ in range(self.max_requests):
                self.workers.append(Worker(self, self.schedulers['Request']))
            for _ in range(self.max_workers):
                self.workers.append(Worker(self, self.schedulers['Default']))
            logger.info('Create %d request workers', self.max_requests)
            logger.info('Create %d workers', self.max_workers)
            self.start_time = time.time()
            self.taskers = {'Request': [], 'Default': []}
            for worker in self.workers:
                if worker.sdl is self.sdl_req:
                    self.taskers['Request'].append(
                        self.loop.create_task(worker.work()))
                else:
                    self.taskers['Default'].append(
                        self.loop.create_task(worker.work()))

        except Exception:
            logger.error(traceback.format_exc())

    async def start_requests(self):
        """Should be rewritten for your custom spider.

        Otherwise it will yield every url in :attr:`start_urls`. Any Request yielded from :meth:`start_requests`
        will combine :meth:`parse` to its callbacks and passes all callbacks to Response
        """
        for url in self.start_urls:
            yield Request(url)

    async def parse(self, response: _Response):
        """ Default callback function for Requests generated by default :meth:`start_requests`.

        Args:
            response: the response task generated from corresponding request.
        """
        yield None

    async def add_task(self, new_task: 'acrawler.task.Task') -> bool:
        """ Interface to add new Task to schedulers.

        Args:
            new_task: a Task or a dictionary which will be catched as :class:`~acrawler.item.DefaultItem` task.

        Returns:
            True if the task is successfully added.
        """
        added = False
        if isinstance(new_task, Task):
            if isinstance(new_task, Request):
                added = await self.sdl_req.produce(new_task)
            else:
                added = await self.sdl.produce(new_task)
        elif isinstance(new_task, dict):
            item = DefaultItem(extra=new_task)
            added = await self.sdl.produce(item)
        if added:
            self.counter.task_add()
        return added

    def _form_config(self):
        # merge configs from three levels of sources
        d_config, d_rq_config, d_m_config = config_from_setting(
            DEFAULT_SETTING)
        try:
            USER_SETTING = import_module('setting')
            u_config, u_rq_config, u_m_config = config_from_setting(
                USER_SETTING)
        except ModuleNotFoundError:
            u_config, u_rq_config, u_m_config = ({}, {}, {})

        self.config = merge_config(
            d_config, u_config, self.config
        )
        self.request_config = merge_config(
            d_rq_config, u_rq_config, self.request_config
        )
        self.middleware_config = merge_config(
            d_m_config, u_m_config, self.middleware_config
        )

    def _logging_config(self):
        # log three types of config
        level = self.config.get('LOG_LEVEL')
        logging.getLogger('acrawler').setLevel(level)
        logger.debug("Merging configs...")
        logger.debug(
            f'config: \n{pformat(self.config)}')
        logger.debug(
            f'request_config: \n{pformat(self.request_config)}')
        logger.debug(
            f'middleware_config:\n {pformat(self.middleware_config)}')

    def _create_schedulers(self):
        # we maintain two schedulers, request task / non-request task.
        self.counter = Counter(loop=self.loop)
        self.redis_enable = self.config.get('REDIS_ENABLE', False)
        self.persistent = self.config.get('PERSISTENT', False)

        request_df = None
        request_q = None
        if self.redis_enable:
            request_df = RedisDupefilter(
                address=self.config.get('REDIS_ADDRESS'),
                df_key=self.config.get('REDIS_DF_KEY')
            )
            request_q = RedisPQ(
                address=self.config.get('REDIS_ADDRESS'),
                q_key=self.config.get('REDIS_QUEUE_KEY')
            )

        self.schedulers = {
            'Request': Scheduler(df=request_df, q=request_q),
            'Default': Scheduler()
        }
        self.sdl = self.schedulers['Default']
        self.sdl_req = self.schedulers['Request']

        self._persist_load()

    def _add_default_middleware_handler_cls(self):
        # append handlers from middleware_config.
        for kv in self.middleware_config.items():
            name = kv[0]
            key = kv[1]
            if key != 0:
                p, h = name.rsplit('.', 1)
                mod = import_module(p)
                mcls = getattr(mod, h)
                mcls.priority = key
                self.middleware.append_handler_cls(mcls)

    async def _on_start(self):
        # call handlers's on_start()
        for sdl in self.schedulers.values():
            await sdl.start()
        logger.info("Call on_start()...")
        for handler in self.middleware.handlers:
            await handler.handle(0)

    async def _on_close(self):
        # call handlers's on_close()
        for sdl in self.schedulers.values():
            await sdl.close()
        logger.info("Call on_close()...")
        for handler in self.middleware.handlers:
            await handler.handle(3)

    async def ashutdown(self, signal=None):
        # shutdown method.
        # 
        # - cancel all Request workers
        # - wait for all nonRequest workers
        # - deal with keyboardinterrupt.
        # - save current status if persistent
        try:
            logger.info(
                'Start shutdown. May take some time to finish Non-Request Task...')
            for tasker in self.taskers['Request']:
                tasker.cancel()

            while await self.sdl.q.get_length() != 0:
                await asyncio.sleep(0.5)

            for tasker in self.taskers['Request']:
                try:
                    await tasker
                except asyncio.CancelledError:
                    pass
            await self._log_status()
            await self._on_close()
            self._persist_save()
            if signal:
                self.run_task.cancel()

            logger.info('Shutdown crawler gracefully!')
            logger.info("End crawling...")
            self.loop.stop()
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.warning('Errors during shutdown')
            self.loop.stop()

    def _persist_load(self):
        if self.persistent and not self.redis_enable:
            tag = self.config.get(
                'PERSISTENT_NAME', None) or self.__class__.__name__
            fname = '.' + tag
            self.fi_tasks: Path = Path.cwd() / ('acrawler' + fname + '.tasks')
            self.fi_df: Path = Path.cwd() / ('acrawler' + fname + '.df')
            if self.fi_tasks.exists():
                with open(self.fi_tasks, 'rb') as f:
                    tasks = pickle.load(f)
                logger.info('Load {} tasks from local file {}.'.format(
                    len(tasks), self.fi_tasks))
                for t in tasks:
                    self.sdl_req.q.push_nowait(t)
                    self.counter.task_add()
            if self.fi_df.exists():
                with open(self.fi_df, 'rb') as f:
                    self.sdl_req.df = pickle.load(f)
                logger.info('Load Dupefilter from {}'.format(self.fi_df))

    def _persist_save(self):
        if self.persistent and not self.redis_enable:
            tasks = []
            with open(self.fi_tasks, 'wb') as f:
                while(1):
                    try:
                        t = self.sdl_req.q.pq.get_nowait()[1]
                        tasks.append(t)
                    except asyncio.QueueEmpty:
                        break
                while(1):
                    try:
                        t = self.sdl_req.q.waiting.get_nowait()[1]
                        tasks.append(t)
                    except asyncio.QueueEmpty:
                        break
                pickle.dump(tasks, f)
            logger.info('Dump {} tasks into local file {}.'.format(
                len(tasks), self.fi_tasks))

            with open(self.fi_df, 'wb') as f:
                pickle.dump(self.sdl_req.df, f)
            logger.info('Dump Dupefilter to {}'.format(self.fi_df))

    async def _log_status_timer(self):
        while True:
            await asyncio.sleep(20)
            await self._log_status()

    async def _log_status(self):
        time_delta = time.time() - self.start_time
        logger.info(f'Statistic: working {time_delta:.2f}s')
        for family in self.counter.counts.keys():
            success = self.counter.counts[family][1]
            failure = self.counter.counts[family][0]
            logger.info(
                f'Statistic:{family:<15} ~ success {success}, failure {failure}')
        logger.info('Normal  Scheduler tasks left:{}'.format(await self.sdl.q.get_length()))
        logger.info('Request Scheduler tasks left:{}'.format(await self.sdl_req.q.get_length()))

    def __getstate__(self):
        # disable pickling
        return {}


class CrawlerStart(SpecialTask):
    """ A special task that executes when crawler starts.

    It will call :meth:`Crawler.start_requests` to yield tasks.
    """

    def __init__(self, crawler):
        self.crawler = crawler
        super().__init__()

    async def _execute(self):
        await self._produce_tasks()

    async def _produce_tasks(self):
        logger.info("Produce initial tasks...")
        async for task in to_asyncgen(self.crawler.start_requests):
            if isinstance(task, Request):
                task.add_callback(self.crawler.parse)
                if await self.crawler.schedulers['Request'].produce(task):
                    self.crawler.counter.task_add()


class CrawlerFinish(SpecialTask):
    """A special task that executes after creating all workers.

    It will block the crawler from shutdown until all tasks finish.
    """

    def __init__(self, crawler):
        self.crawler = crawler
        super().__init__()

    async def _execute(self):
        await self._wait_finished()

    async def _wait_finished(self):
        await self.crawler.counter.join()
