import asyncio
import unittest
from unittest import mock

import chat
import pipeline


class Client(chat.Client):
    def __init__(self, name):
        self.name = name
        self.send_queue = asyncio.Queue()
        self.recv_queue = asyncio.Queue()
    def add_request(self, request):
        self.recv_queue.put_nowait(self.name + request)
    async def receive_response(self):
        response = await self.recv_queue.get()
        return response


class TestPipeline(unittest.IsolatedAsyncioTestCase):

    async def test_test(self):
        """Smoke test for the test framework."""
        client = Client("foo")
        await client.start()
        client.add_request("one")
        self.assertEqual(await client.receive_response(), "fooone")
        client.add_request("two")
        client.add_request("three")
        self.assertEqual(
            await client.receive_response(), "footwo")
        self.assertEqual(
            await client.receive_response(), "foothree")
        try:
            await asyncio.wait_for(
                client.receive_response(), timeout=1)
        except asyncio.TimeoutError:
            pass

    async def test_compose(self):
        client_foo = Client("foo")
        client_bar = Client("bar")
        client = pipeline.Composer(client_foo, client_bar)
        await client.start()
        client.add_request("one")
        self.assertEqual(
            await client.receive_response(), "barfooone")
        client.add_request("two")
        client.add_request("three")
        self.assertEqual(
            await client.receive_response(), "barfootwo")
        self.assertEqual(
            await client.receive_response(), "barfoothree")
        try:
            await asyncio.wait_for(
                client.receive_response(), timeout=1)
        except asyncio.TimeoutError:
            pass


if __name__ == '__main__':
    unittest.main()
