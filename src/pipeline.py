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
            self.consumer.add_request(
                await self.producer.receive_response())

    def receive_response(self):
        return self.consumer.receive_response()


class HumanPipeline():
    """
    Container for pipelines.
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


class ReplicantPipeline():
    """
    Container for pipelines.
    """

    def __init__(self, socket):

        # Line to transcribe chunks to lines, and not output anything.
        self.lines_line = lines.Client(socket, silent=True)
        # Line to create bot text, transcribe to lines, and output chunks.
        self.lines_speech_line = Composer(
            lines.Client(socket, bot=True), speech.Client())
        self.bot_line = Composer(
            chat.BotClient(), self.lines_speech_line)

    async def start(self):
        await self.lines_line.start()
        await self.bot_line.start()

    def stop(self):
        self.lines_line.stop()
        self.bot_line.stop()

    def add_request(self, request):
        self.line_line.add_request(request)
        self.bot_line.add_request(request)

    def receive_response(self):
        return self.bot_line.receive_response()


class BotPipeline():
    """
    Container for a pipeline for string requests and chunk responses.
    """
    # This container is unnecessary, because we only call the methods
    # which are directly passed to the composer.

    def __init__(self, socket):
        self.lines_speech_line = Composer(
            lines.Client(socket), speech.Client())
        self.line = Composer(
            chat.Client(), self.lines_speech_line)

    def start(self):
        return self.line.start()

    def stop(self):
        return self.line.stop()

    def add_request(self, request):
        return self.line.add_request(request)

    def receive_response(self):
        return self.line.receive_response()

