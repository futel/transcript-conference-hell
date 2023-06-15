#!/usr/bin/env python

import asyncio
import base64
import json
import random
import time
import uuid
import websockets

import chat
import pipeline
import lines
import util

#host = "localhost"
port = 6000

# The name of the bot in the transcripts.
chat_label = "Franz"
# Bot may nag humans if population is fewer than this.
min_population = 3


class Program:
    """
    Holds methods and attributes relevant to bot interaction and
    pipelines for bots and humans.
    """

    async def bot_line(self, population, transcript_lines):
        """Return a line from the bot."""
        raise NotImplementedError

    def recent_bot_line(self, transcript_lines):
        """
        Return True if there aren't yet enough bot lines, or
        the bot has a recent line, in transcript_lines.
        """
        labels = lines.line_labels(transcript_lines)
        try:
            for label in [labels.pop(), labels.pop()]:
                if label == chat_label:
                    # One of the last two lines are bot lines.
                    return True
        except IndexError:
            return True
        return False

    def should_bot_line(self, transcript_lines):
        """Return True if the bot should talk."""
        if self.recent_bot_line(transcript_lines):
            return False
        # Half chance of bot line.
        if random.choice([True, False]):
            return True
        return False

    async def bot_line_or_none(self, population, transcript_lines):
        """
        Return a chat line or None.
        """
        if self.should_bot_line(transcript_lines):
            return await self.bot_line(population, transcript_lines)
        return None


class ChatProgram(Program):
    """
    Chats with humans.
    """
    async def bot_line(self, population, transcript_lines):
        """Return a line from the bot."""
        if population < min_population:
            # Half chance of nagging.
            if random.choice([True, False]):
                return chat.nag_string()
        # We didn't nag, return a chat line.
        return await chat.chat_line(transcript_lines)


class PoetryProgram(Program):
    """
    Recites poetry with humans.
    """
    async def bot_line(self, population, transcript_lines):
        """Return a line from the bot."""
        # XXX we might want to nag or contribute.
        # XXX testing
        return await chat.chat_line(transcript_lines)

    def should_bot_line(self, transcript_lines):
        """
        Return True if the bot should reply to a prompt and maybe talk.
        """
        # We always want a bot line, even if we don't return it.
        if self.recent_bot_line(transcript_lines):
            # XXX possible success/fail notify here
            return False
        return True


class Socket:
    def __init__(self, websocket):
        self.websocket = websocket
        self.line = None
        self.stream_sid = None


class FakeSocket:
    """Object to hold a line and a stream_sid identifier."""
    stream_sid = chat_label


class Server:
    def __init__(self):
        """Yields media chunks with recieve_media()."""
        self.server = None
        self.sockets = set()
        self.chat_socket = None
        self.program = PoetryProgram()

    async def start(self):
        util.log("websocket server starting")
        await self.fake_handler()
        await self.periodic_task()
        self.server = await websockets.serve(self.handler, port=port)

    # async def stop(self):
    #     await self.server.close()
    #     raise NotImplementedError

    async def periodic_task(self):
        """Return a task to do the periodic things."""
        async def p_d():
            while True:
                # Send a chat line if we have one.
                population = len(self.sockets)
                transcript_lines = lines.read_lines()
                line = await self.program.bot_line_or_none(
                    population, transcript_lines)
                if line:
                    self.chat_socket.line.add_request(line)
                await asyncio.sleep(10)
        return asyncio.create_task(p_d())

    def _message_to_chunk(self, message):
        return base64.b64decode(message["media"]["payload"])

    # def mark_message(self):
    #     """
    #     Return a mark message which can be sent to the Twilio websocket.
    #     """
    #     return {"event": "mark",
    #             "streamSid": self._stream_sid,
    #             "mark": {"name": uuid.uuid4().hex}}

    async def get_pipeline(self, socket):
        """ Return a client pipeline for chunk requests and responses."""
        line = pipeline.HumanPipeline(socket)
        await line.start()
        return line

    def add_request(self, socket, request):
        """Add request to socket's speech pipeline."""
        socket.line.lines_speech_line.add_request(request)

    async def consumer_handler(self, socket):
        """
        Handle every message in socket's websocket until we receive a stop
        message or barf.
        """
        util.log("websocket connection opened")
        async for message in socket.websocket:
            message = json.loads(message)
            if message["event"] == "connected":
                util.log(
                    f"websocket received event 'connected': {message}")
            elif message["event"] == "start":
                util.log(f"websocket received event 'start': {message}")
                socket.stream_sid = message['streamSid']
                request = chat.hello_string()
                self.add_request(socket, request)
            elif message["event"] == "media":
                # util.log("Received event 'media'")
                # This assumes we get messages in order, we should instead
                # verify the sequence numbers? Or just skip?
                # message["sequenceNumber"]
                socket.line.add_request(self._message_to_chunk(message))
            elif message["event"] == "stop":
                util.log(f"websocket received event 'stop': {message}")
                request = chat.goodbye_string()
                self.add_request(socket, request)
                break
            elif message["event"] == "mark":
                util.log(f"websocket received event 'mark': {message}")
        util.log("websocket connection closed")

    async def send(self, socket, chunk):
        """Send chunk to websocket in a media message."""
        payload = base64.b64encode(chunk).decode()
        await socket.websocket.send(
            json.dumps(
                {"event": "media",
                 "streamSid": socket.stream_sid,
                 "media": {"payload": payload}}))

    async def producer_handler(self, socket):
        """
        Iterate over messages from socket's line, and send them to
        the other websockets.
        """
        while True:
            chunk = await socket.line.receive_response()
            for s in self.sockets:
                if s != socket:
                    await self.send(s, chunk)
                    util.log(
                        f"websocket sent response from "
                        "{socket.stream_sid} to {s.stream_sid}")
            # We could do the bot response here instead of periodically.

    async def handler(self, websocket):
        """
        Set up, run, and tear down consumer and producer tasks
        for this websocket connection.
        """
        util.log("websocket connection opened")
        socket = Socket(websocket)
        socket.line = await self.get_pipeline(socket)
        self.sockets.add(socket)
        util.log("websocket connections: {}".format(len(self.sockets)))
        done, pending = await asyncio.wait(
            [asyncio.create_task(self.consumer_handler(socket)),
             asyncio.create_task(self.producer_handler(socket))],
            return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()
        socket.line.stop()
        self.sockets.remove(socket)
        util.log("websocket connection closed")

    async def get_fake_handler_pipeline(self, socket):
        """
        Return a client pipeline for string requests and chunk responses.
        """
        line = pipeline.BotPipeline(socket)
        await line.start()
        return line

    async def fake_handler(self):
        """
        Set up and run a producer task without a consumer.
        """
        # This isn't really a handler, because there is no consumer
        # callback. The fake chat_socket recives requests directly from
        # a task.
        socket = FakeSocket()
        socket.line = await self.get_fake_handler_pipeline(socket)
        self.chat_socket = socket
        # We don't clean this up, we should do that in stop().
        asyncio.create_task(self.producer_handler(socket))

    async def change_program(self, program):
        """Replace program, and all pipelines with appropriate ones."""
        self.chat_socket.line.stop()
        self.chat_socket.line = await self.get_fake_handler_pipeline(
            socket)
        for socket in self.sockets:
            socket.line.stop()
            socket.line = await self.get_pipeline(socket)
        self.program = program
