"""Client to write attibuted transcription lines."""

import asyncio

import util

def write_line(line):
    # Q&D test, log the line.
    util.log("{}: {}".format(line.label, line.content), 'lines')

def read_lines():
    try:
        with open('/tmp/lines', 'r') as f:
            return [line_from_str(line) for line in f.readlines()]
    except FileNotFoundError:
        return []

def line_from_str(text):
    (label, content) = text.split(':')
    label = label.strip()
    content = content.strip()
    return Line(label, content)


class Line():
    """A transcript line."""
    def __init__(self, label, content, ordinal=None):
        self.label = label
        self.content = content
        self.ordinal = ordinal

    def __str__(self):
        # Q&D, log the line.
        util.log("{}: {}".format(self.label, self.content), 'lines')


class Client():
    """Client to write transcript lines."""
    def __init__(self, socket):
        # We only want the stream_sid, but we have to store the socket
        # because it doesn't have it yet.
        self.socket = socket
        self.recv_queue = asyncio.Queue()
    async def start(self):
        pass
    def stop(self):
        pass
    def add_request(self, text):
        # Q&D test, log the line.
        write_line(Line(self.socket.stream_sid, text))
        self.recv_queue.put_nowait(text)
    def receive_response(self):
        return self.recv_queue.get()
