import asyncio

from collections import deque

class SongQueue:
    def __init__(self):
        self.queue = deque()
        self.loop_mode = "1"
        self._queue_event = asyncio.Event()

    async def put(self, item):
        self.queue.append(item)
        self._queue_event.set()
        
    @property
    def is_empty(self):
        return len(self.queue) == 0

    async def get(self):
        while not self.queue:
            self._queue_event.clear()
            await self._queue_event.wait()
        
        return self.queue.popleft()

    async def clear(self):
        self.queue.clear()

    def appendleft_current(self, item):
        self.queue.appendleft(item)

    def append_current(self, item):
        self.queue.append(item)