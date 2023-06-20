#!/usr/bin/env python

import asyncio
import base64
import json
import time
import uuid
import websockets

import chat
import pipeline
import program
import lines
import util

#host = "localhost"
port = 6000


class Socket:
    def __init__(self, websocket):
        self.websocket = websocket
        self.line = None
        self.stream_sid = None

    async def get_pipeline(self, prog):
        self.line = prog.get_pipeline(self)
        await self.line.start()

    def add_request(self, request):
        return self.line.add_request({'chunk': request['chunk']})

    def add_speech_request(self, request):
        return self.line.line_speech_line.add_request({'text': request['text']})

    def receive_response(self):
        return self.line.receive_response()

    def stop(self):
        return self.line.stop()


class FakeSocket:
    """Object to hold a line and a stream_sid identifier."""
    stream_sid = chat.chat_label

    async def get_pipeline(self):
        self.line = pipeline.BotPipeline(self)
        await self.line.start()

    def add_request(self, request):
        return self.line.add_request({'text': request['text']})

    def stop(self):
        return self.line.stop()

    def receive_response(self):
        return self.line.receive_response()


class Server:
    def __init__(self):
        """Yields media chunks with recieve_media()."""
        self.server = None
        self.sockets = set()
        self.chat_socket = None
        self.program = program.ChatProgram()

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
                population = len(self.sockets)
                if population:
                    # Send a chat line if we have one.
                    transcript_lines = lines.read_lines()
                    for line in await self.program.bot_lines(
                            population, transcript_lines):
                        self.chat_socket.add_request(line)
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
                socket.add_speech_request({'text':request})
            elif message["event"] == "media":
                # This assumes we get messages in order, we should instead
                # verify the sequence numbers? Or just skip?
                # message["sequenceNumber"]
                socket.add_request({'chunk': self._message_to_chunk(message)})
            elif message["event"] == "stop":
                util.log(f"websocket received event 'stop': {message}")
                request = chat.goodbye_string()
                socket.add_speech_request({'text':request})
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
            chunk = await socket.receive_response()
            chunk = chunk['chunk']
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
        await socket.get_pipeline(self.program)
        self.sockets.add(socket)
        util.log("websocket connections: {}".format(len(self.sockets)))
        done, pending = await asyncio.wait(
            [asyncio.create_task(self.consumer_handler(socket)),
             asyncio.create_task(self.producer_handler(socket))],
            return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()
        socket.stop()
        self.sockets.remove(socket)
        util.log("websocket connection closed")

    async def fake_handler(self):
        """
        Set up and run a producer task without a consumer.
        """
        # This isn't really a handler, because there is no consumer
        # callback. The fake chat_socket recives requests directly from
        # a task.
        socket = FakeSocket()
        await socket.get_pipeline()
        self.chat_socket = socket
        # We don't clean this up, we should do that in stop().
        asyncio.create_task(self.producer_handler(socket))

    async def change_program(self, prog):
        """Replace program, and all pipelines with appropriate ones."""
        self.program = prog
        self.chat_socket.stop()
        await self.chat_socket.get_pipeline()
        for socket in self.sockets:
            socket.stop()
            await socket.get_pipeline(self.program)

