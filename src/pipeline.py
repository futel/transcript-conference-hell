import asyncio

import chat
import lines
import speech
import transcription


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
        while True:
            self.consumer.add_request(await self.producer.receive_response())

    def receive_response(self):
        return self.consumer.receive_response()


class HumanPipeline():
    """
    Container for a pipeline for chunk requests and responses.
    """

    def __init__(self, socket):
        self.lines_speech_line = Composer(
            lines.Client(socket), speech.Client())
        self.line = Composer(
            transcription.Client(), self.lines_speech_line)

    def start(self):
        return self.line.start()

    def stop(self):
        return self.line.stop()

    def add_request(self, request):
        return self.line.add_request(request)

    def receive_response(self):
        return self.line.receive_response()


class BotPipeline():
    """
    Container for a pipeline for string requests and chunk responses.
    """

    def __init__(self, socket):
        line = Composer(chat.Client(), lines.Client(socket))
        self.line = Composer(line, speech.Client())

    def start(self):
        return self.line.start()

    def stop(self):
        return self.line.stop()

    def add_request(self, request):
        return self.line.add_request(request)

    def receive_response(self):
        return self.line.receive_response()

