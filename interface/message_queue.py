from asyncio import Queue
from collections import defaultdict

class MessageQueueManager:
    def __init__(self):
        self.queues = defaultdict(Queue)

    def get_queue(self, code):
        return self.queues[code]

    def create_queue(self, code):
        if code not in self.queues:
            self.queues[code] = Queue()
            print(f"Created queue for code: {code}")

    def delete_queue(self, code):
        if code in self.queues:
            del self.queues[code]
            print(f"Deleted queue for code: {code}")

    async def add_message(self, code, message):
        if code in self.queues:
            await self.queues[code].put(message)
            print(f"Added message to code {code}: {message}")
        else:
            print(f"Queue for code {code} does not exist")