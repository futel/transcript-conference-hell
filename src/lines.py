"""Read and write transcription lines."""

import asyncio
import copy
import datetime
import itertools
import json

import util

def write_line(line):
    """Format and log the line."""
    d = copy.copy(line.__dict__)
    d['timestamp'] = datetime.datetime.now().isoformat()
    util.log(str(line), 'lines')

def get_lines():
    try:
        return open('/tmp/lines', 'r').readlines()
    except FileNotFoundError:
        return []

def line_from_str(text):
    return Line(**json.loads(text))

def read_lines():
    counter = itertools.count()
    def ordinaler(line):
        line.ordinal = next(counter)
        return line
    lines = get_lines()
    try:
        return [ordinaler(line_from_str(line)) for line in lines]
    except Exception as e:
        util.log('read_lines exception {}'.format(e))
        util.log('read_lines lines {}'.format(lines))
        return []

class Line():
    """A transcript line."""
    def __init__(self, label, content, ordinal=None, **attributes):
        self.label = label
        self.content = content
        self.ordinal = ordinal
        for attr in attributes:
            setattr(self, attr, attributes[attr])

    def __repr__(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return self.__repr__()

    def prompt_str(self):
        """Return a string suitable for a chat prompt."""
        return '{}: {}'.format(self.label, self.content)


class Client():
    """
    Client to write transcript lines with text given in request,
    and pass text to the response.
    """
    def __init__(self, socket, **attributes):
        # We only want the stream_sid, but we have to store the socket
        # because it doesn't have it yet.
        self.socket = socket
        self.recv_queue = asyncio.Queue()
        self.attributes = attributes
    async def start(self):
        pass
    def stop(self):
        pass
    def add_request(self, request):
        """
        Extract text from websocket message, write to transcript,
        and pass to response.
        """
        text = request['text']
        # This is where we log the trasncript of all text which turns to speech,
        # whether transcribed from human speech or from a line sent to a bot.
        write_line(Line(self.socket.stream_sid, text, **self.attributes))
        self.recv_queue.put_nowait(text)
    async def receive_response(self):
        """When we receive text, format and return."""
        return {'text': await self.recv_queue.get()}
