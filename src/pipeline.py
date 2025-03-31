import asyncio

import chat
import lines
import speech
import transcription


class Composer:
    """
    Chains two producer/consumers together to form one
    producer/consumer.
    """
    # There is surely a pattern for this async generator composer
    # that I just don't know the name of.

    def __init__(self, producer, consumer):
        self.producer = producer
        self.consumer = consumer

    async def start(self):
        await self.consumer.start()
        await self.producer.start()
        # We should probably do this on init and not cancel?
        self.step_task = asyncio.create_task(self.step_generator())

    def stop(self):
        self.producer.stop()
        self.consumer.stop()
        # We should probably not cancel?
        self.step_task.cancel()

    def add_request(self, request):
        self.producer.add_request(request)

    async def step_generator(self):
        """
        Async generator to await the receipt of a response from producer
        and send it as a request to consumer.
        """
        while True:
            self.consumer.add_request(
                await self.producer.receive_response())

    def receive_response(self):
        return self.consumer.receive_response()


class HumanPipeline():
    """
    Container for pipelines. Used for input and output of human websocket
    clients. Requests to be added are chunks of audio that the server recieved
    from the client. Responses to be sent are chunks of audio from
    transcription. In between, the audio gets speech to text, is logged, and the
    text gets text to speech.
    """

    def __init__(self, socket):
        """
        Set up my line. Receives audio chunk requests, transcribes, turns
        to speech, sends audio chunk responses.
        """
        # Line for text to audio chunks which transcribes.
        self.line_speech_line = Composer(
            lines.Client(socket), speech.Client())
        # Line for audio chunks to text to line_speech_line
        self.line = Composer(
            transcription.Client(), self.line_speech_line)

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
        # Line to transcribe text to lines, and output chunks.
        self.line_speech_line = Composer(
            lines.Client(socket, bot=True), speech.Client())
        # Line to find transcripts and send to line_speech_line.
        bot_speech_line = Composer(
            chat.BotClient(socket), self.line_speech_line)
        # Line to transcribe text to lines and send to bot_speech_line.
        line_bot_speech_line = Composer(
            lines.Client(socket, silent=True), bot_speech_line)
        # Line to transcribe chunks send to line_bot_speech_line.
        self.line = Composer(transcription.Client(), line_bot_speech_line)

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
    Used by a bot socket to recieve text requests and send speech responses.
    """
    # This container is unnecessary, because we only call the methods
    # which are directly passed to the composer.
    def __init__(self, socket):
        # Interim pipeline, receive text messages, write transcript,
        # respond with speech chunks.
        self.line_speech_line = Composer(
            lines.Client(socket, bot=True), speech.Client())
        # Why do we need to compose a new pipeline? Doesn't chat.Client just
        # pass requests to responses? Is this why this container is
        # unnecessary?
        self.line = Composer(
            chat.Client(), self.line_speech_line)

    def start(self):
        return self.line.start()

    def stop(self):
        return self.line.stop()

    def add_request(self, request):
        return self.line.add_request(request)

    def receive_response(self):
        return self.line.receive_response()
