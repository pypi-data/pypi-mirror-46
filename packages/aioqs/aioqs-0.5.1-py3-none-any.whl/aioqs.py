'''
Created on 21 мая 2019 г.

@author: wwolf <wWolfovich@gmail.com>
'''

import asyncio

class AIOQS(object):
    def __init__(self, work, limit=0, loop=None):
        self._tasks = work
        self._loop = loop if loop else asyncio.get_event_loop()
        self._semaphore = asyncio.Semaphore(limit) if limit >= 0 else None
        self._queue = asyncio.queues.Queue(loop=self._loop)
        self._pool = set()
        self._ff = None
        self._event = asyncio.locks.Event()


    async def add(self, coro):
        if self._semaphore:
            await self._semaphore.acquire()
        
        fut = asyncio.ensure_future(coro)
        self._pool.add(fut)
        fut.add_done_callback(self._on_done)


    def _on_done(self, fut):
        self._queue.put_nowait(fut)
        self._event.set()
        self._pool.remove(fut)
        if self._semaphore: self._semaphore.release()
        if not self._pool and self._ff.done(): self._queue.put_nowait(StopIteration())


    async def __aenter__(self):
        return self


    async def __aexit__(self):
        asyncio.gather(*self._pool)
        
        
    async def __run(self):
        for f in self._tasks:
            await self.add(f)
        if self._pool: asyncio.gather(*self._pool)


    def __aiter__(self):
        self._ff = asyncio.ensure_future(self.__run())
        return self


    async def __anext__(self):
        fut = await self._queue.get()
        if isinstance(fut, StopIteration):
            raise StopAsyncIteration
        else:
            return fut
