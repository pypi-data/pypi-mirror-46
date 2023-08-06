'''
Created on 21 мая 2019 г.

@author: wwolf <wWolfovich@gmail.com>
'''

import asyncio
try:
    from async_timeout import timeout as async_timeout
    async def wait_for(coro, timeout=0):
        async with await async_timeout(timeout):
            return await coro


except ModuleNotFoundError:
    from asyncio import wait_for

class AIOQS(object):
    """Async queue/schedule with limit for running tasks.
    With no overhead on tracking workers state but it runs and set in queue
    @param work: iterable of coroutines
    @param limit: number of running tasks
    @param loop: for compatibility with other async modules"""
    
    def __init__(self, work, limit=0, loop=None):
        self._tasks = work
        self._loop = loop if loop else asyncio.get_event_loop()
        self._semaphore = asyncio.Semaphore(limit) if limit >= 0 else None
        self._queue = asyncio.queues.Queue(loop=self._loop)
        self._pool = set()
        self._ff = None
        self._event = asyncio.locks.Event()
        
        # Method override
        self.add = self.__lim_add if self._semaphore else self.__add

    async def __lim_add(self, coro):
        """Wrapper method around self.__add used when @param limit is set"""
        await self._semaphore.acquire()
        self.__add(coro)


    async def __add(self, coro):
        """Adding coro-worker to pool"""
        fut = asyncio.ensure_future(coro)
        self._pool.add(fut)
        fut.add_done_callback(self._on_done)


    def _on_done(self, fut):
        """Coroutines done-callback"""
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
        """Run though tasks iterable adding jobs to pool
        and wait for all of them to finish"""
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
