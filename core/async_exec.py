# *-* coding: utf-8 *-*

import multiprocessing

from concurrent.futures import ThreadPoolExecutor

from tornado.concurrent import Future, chain_future
from tornado.ioloop import IOLoop


class AsyncExecution:
    def __init__(self, max_workers=None):
        self._max_workers = max_workers or multiprocessing.cpu_count()
        self._pool = None

    def set_max_workers(self, count):
        if self._pool:
            self._pool.shutdown(wait=True)

        self._max_workers = count
        self._pool = ThreadPoolExecutor(max_workers=self._max_workers)

    def as_future(self, query):
        if not self._pool:
            self._pool = ThreadPoolExecutor(max_workers=self._max_workers)

        old_future = self._pool.submit(query)
        new_future = Future()

        IOLoop.current().add_future(old_future,
                                    lambda f: chain_future(f, new_future))

        return new_future


as_future = AsyncExecution().as_future