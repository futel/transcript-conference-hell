"""Read and write transcription lines."""

import asyncio
import itertools
import json

import util

def write_line(line):
    # Q&D test, log the line.
    util.log(str(line), 'lines')

def read_lines():
    counter = itertools.count()
    def ordinaler(line):
        line.ordinal = next(counter)
        return line
    try:
        with open('/tmp/lines', 'r') as f:
            return [
                ordinaler(line_from_str(line)) for line in f.readlines()]
    except FileNotFoundError:
        return []

def line_from_str(text):
    return Line(**json.loads(text))
    #(label, content) = text.split(':')
    #label = label.strip()
    #content = content.strip()
    #return Line(label, content, ordinal)


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
    Client to write transcript lines using given text,
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
        text = request['text']
        write_line(Line(self.socket.stream_sid, text, **self.attributes))
        self.recv_queue.put_nowait(text)
    async def receive_response(self):
        return {'text': await self.recv_queue.get()}
