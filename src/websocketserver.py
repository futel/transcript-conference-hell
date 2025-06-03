"""
Websocket server. Instantiate Server, run start, wait for async events and
tasks.
"""

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
import speech
import util

#host = "localhost"
port = 6000

# Seconds between periodic task runs.
bot_period = 5
victory_period = 1

program_cycle = program.next_program()


class Socket:
    def __init__(self, websocket):
        # Websocket to send and receive messages to/from the client.
        self.websocket = websocket
        # Client to send speech directly to myself.
        self.speech = speech.Client()
        self.stream_sid = None
        # Pipeline to receive my audio chunks and send responses to the server.
        self.line = pipeline.HumanPipeline(self)
        self.attrs = {}

    async def start(self, prog):
        # XXX we have to handle replacing the pipeline to do this
        #self.line = prog.get_pipeline(self)
        await self.line.start()
        self.speech_handler_task = asyncio.create_task(
            self.consumer_handler())
        await self.speech.start()

    def stop(self):
        self.speech.stop()
        self.speech_handler_task.cancel()
        self.line.stop()

    def add_request(self, request):
        """
        Add audio chunk to my pipeline.
        Called by the server when this client has sent a media message, the
        request contains the chunk.
        """
        return self.line.add_request({'chunk': request['chunk']})

    def add_speech_request(self, request):
        """
        Send text directly to the middle of my pipeline as if the pipeline made
        it from an audio request sent to the beginning.
        """
        return self.line.line_speech_line.add_request(
            {'text': request['text']})

    def add_self_speech_request(self, request):
        """
        Send text request to my speech line, to turn into a response to me.
        """
        return self.speech.add_request({'text': request['text']})

    def receive_response(self):
        """
        Get audio chunk from my pipeline. Happens when the audio initially sent
        by the client has gone through my pipeline and a response is ready.
        """
        return self.line.receive_response()

    def send(self, chunk):
        """
        Send chunk to websocket in a media message, to be played for the client.
        """
        payload = base64.b64encode(chunk).decode()
        return self.websocket.send(
            json.dumps(
                {"event": "media",
                 "streamSid": self.stream_sid,
                 "media": {"payload": payload}}))

    async def consumer_handler(self):
        """Send all responses from my personal speech line to myself."""
        while True:
            response = await self.speech.receive_response()
            await self.send(response['chunk'])


class FakeSocket:
    """
    Holds a BotPipeline to receive bot chat lines, and a stream_sid identifier.
    Send chat to this for bot speech responses that can be sent to sockets.
    """
    # This is not a real stream SID. We have no stream. The real sockets
    # re-use this as a label in the transcript.
    stream_sid = chat.chat_label

    def __init__(self):
        self.line = pipeline.BotPipeline(self)

    async def start(self):
        await self.line.start()

    def add_request(self, request):
        return self.line.add_request({'text': request['text']})

    def stop(self):
        self.line.stop()

    def receive_response(self):
        return self.line.receive_response()


class Server:
    """
    Websocket server. Run start(), then wait for async events and tasks.
    Holds client sockets.
    Holds a fake chat socket to send bot chunks to sockets.
    Holds the program, checks for victory, cycles programs.
    """

    def __init__(self):
        self.server = None
        self.sockets = set()
        self.chat_socket = None
        self.latest_stream_sid = None
        # Start with an arbitrary program.
        self.program = program.ArithmeticProgram()

    async def start(self):
        """
        Set up the fake chat socket to receive bot text lines and send chunks to
        client sockets.
        Start the task to check for victory conditions.
        Start the server with our handler method.
        """
        util.log("websocket server starting")

        # Set up the fake bot socket to send speech.
        await self.fake_handler()
        # Set up the task to send periodic text lines to the fake bot socket.
        await self.bot_line_task()
        # Set up the task to check for and respond to victory conditions.
        await self.victory_task()
        # We are ready, start the server by declaring the handler.
        self.server = await websockets.serve(self.handler, port=port)
        util.log("websocket server started")

    async def stop(self):
        # Hopefully this never happens, we leak everything.
        util.log("websocket server stopping")
        await self.server.close()
        util.log("websocket server stopped")

    async def bot_line_task(self):
        """
        Return a task to periodically check for and send bot text lines to our
        chat_socket.
        """
        async def f():
            while True:
                # This try/except should be handled around the task run?
                try:
                    population = len(self.sockets)
                    if population:
                        # If the program has lines to send, send them.
                        transcript_lines = lines.read_lines()
                        for line in await self.program.bot_lines(
                                population, transcript_lines, self):
                            self.chat_socket.add_request({'text': line})
                except Exception as e:
                    util.log('bot line task exception {}'.format(e))
                    raise       # XXX testing
                await asyncio.sleep(bot_period)
        return asyncio.create_task(f())

    async def victory_task(self):
        """
        Return a task to periodically check for and do victory actions.
        """
        async def f():
            while True:
                population = len(self.sockets)
                if population:
                    if self.program.victory:
                        await self.change_program(next(program_cycle))
                await asyncio.sleep(victory_period)
        return asyncio.create_task(f())

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
            # if message["event"] == "connected":
            #     pass
            # elif message["event"] == "mark":
            #     pass
            if message["event"] == "start":
                # New client enter message. Set up socket, send
                # intro requests.
                socket.stream_sid = message['streamSid']
                # Send text to socket to speak to itself.
                population = len(self.sockets)
                socket.add_self_speech_request(
                    {'text': self.program.intro_text(socket, population)})
                # Send text for socket to speak to other clients.
                request = chat.hello_string()
                socket.add_speech_request({'text':request})
            elif message["event"] == "media":
                # Audio chunk from client. Give it to the client's pipeline.
                # This assumes we get messages in order, we should instead
                # verify the sequence numbers? Or just skip?
                # message["sequenceNumber"]
                socket.add_request(
                    {'chunk': self._message_to_chunk(message)})
            elif message["event"] == "stop":
                # Client exit message. Send outro request.
                request = chat.goodbye_string()
                # Send text for socket to speak to other clients.
                socket.add_speech_request({'text':request})
                break
            elif message["event"] == "dtmf":
                # DTMF message from client.
                util.log('dtmf message {}'.format(message['dtmf']['digit']))
                util.log('latest_stream_sid {}'.format(self.latest_stream_sid))
                # Find the latest socket that sent audio.
                latest_socket = next(
                    (s for s in self.sockets
                     if s.stream_sid == self.latest_stream_sid),
                    None)
                util.log('xxx latest_socket {}'.format(getattr, latest_socket, '__dict__', None))
                # Have the program perform any DTMF reaction, and send any
                # strings it returns to the chat socket to speak.
                for line in self.program.handle_dtmf(
                        message, socket, latest_socket, self.sockets):
                    self.chat_socket.add_request({'text': line})

        util.log("websocket connection closed")

    async def producer_handler(self, socket):
        """
        Iterate over messages received from socket's line, and send their chunks
        to the other websockets.
        """
        while True:
            chunk = await socket.receive_response()
            # The socket is now the most recent which has sent audio.
            self.latest_stream_sid = socket.stream_sid
            # We assume that every message has a chunk.
            chunk = chunk['chunk']
            for s in self.sockets:
                if s != socket:
                    await s.send(chunk)
                    #util.log("sent chunk from {} to {}".format(
                    #    socket.stream_sid, s.stream_sid))
            # We could do the bot response here instead of periodically.

    async def handler(self, websocket):
        """
        Set up, run, then tear down consumer and producer tasks
        for this websocket connection. Called when a new connection opens.
        """
        util.log("websocket connection opened")
        socket = Socket(websocket)
        await socket.start(self.program)
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
        population = len(self.sockets)
        util.log("websocket connections: {}".format(population))
        if not population:
            # Nobody is connected, change the program.
            await self.change_program(next(program_cycle))

    async def fake_handler(self):
        """
        Set up a FakeSocket on our chat_socket attribute, where it can receive
        bot text lines. Run a producer task for it to send speech chunks to
        the client sockets.
        """
        # This isn't really a handler, because there is no consumer
        # callback. The fake chat_socket recives requests directly from
        # a task.
        socket = FakeSocket()
        await socket.start()
        self.chat_socket = socket
        # Start a task with the producer_handler just like our websockets do
        # when they connect, so that when the chat_socket gets text, it
        # sends chunks to all the other client sockets.
        # We don't clean this up, we should do that in stop(), but we don't
        # expect that to actually happen.
        asyncio.create_task(self.producer_handler(socket))

    async def change_program(self, prog_class):
        """Replace program, and all pipelines with appropriate ones."""
        util.log("changing program to {}".format(prog_class))
        util.log("lines: {}".format(lines.read_lines()))
        # Send transcript logfile to s3, then clear it.
        util.write_lines_s3()
        util.clear_lines()
        # Change the program.
        self.program = prog_class()
        self.chat_socket.stop()
        await self.chat_socket.start()
        succeed_str = chat.general_succeed_string()
        # Send speech to all clients to say we are changing programs.
        population = len(self.sockets)
        for socket in self.sockets:
            socket.stop()
            await socket.start(self.program)
            socket.add_self_speech_request({'text': succeed_str})
            socket.add_self_speech_request(
                {'text': self.program.intro_text(socket, population)})
