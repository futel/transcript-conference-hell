import asyncio

class Composer:
    """
    Chains two producer/consumers together to form one
    producer/consumer"""
    # There is surely a pattern for this async generator composer
    # that I just don't know the name of.

    def __init__(self, producer, consumer):
        self.producer = producer
        self.consumer = consumer
        self.step_task = asyncio.create_task(self.step_generator())

    async def start(self):
        await self.consumer.start()
        await self.producer.start()

    def stop(self):
        self.producer.stop()
        self.consumer.stop()
        self.step_task.cancel()

    def add_request(self, request):
        self.producer.add_request(request)

    async def step_generator(self):
        """
        Async generator to receive from producer and send to consumer.
        """
        async for item in self.producer.receive_response():
            self.consumer.add_request(item)

    async def receive_response(self):
        async for response in self.consumer.receive_response():
            yield response
