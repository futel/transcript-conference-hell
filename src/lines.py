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

def line_from_str(text, ordinal=None):
    (label, content) = text.split(':')
    label = label.strip()
    content = content.strip()
    return Line(label, content, ordinal)


class Line():
    """A transcript line."""
    def __init__(self, label, content, ordinal=None, **attributes):
        self.label = label
        self.content = content
        self.ordinal = ordinal
        self.attributes = attributes

    def __repr__(self):
        return json.dumps(
            dict(label=self.label, content=self.content, **self.attributes))
    def __str__(self):
        return self.__repr__()


class Client():
    """
    Client to write transcript lines using given text,
    and possibly pass alt_text.
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
    def add_request(self, text=None, alt_text=None):
        write_line(Line(self.socket.stream_sid, text, self.attributes))
        if alt_text:
            self.recv_queue.put_nowait((text, alt_text))
        else:
            self.recv_queue.put_nowait(text)
    def receive_response(self):
        return self.recv_queue.get()

class ReplicantClient():
    """Client to write transcript lines using given alt_text."""
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
    def add_request(self, text, alt_text=None):
        write_line(
            Line(self.socket.stream_sid, alt_text, self.attributes))
        self.recv_queue.put_nowait(alt_text)
    def receive_response(self):
        return self.recv_queue.get()
