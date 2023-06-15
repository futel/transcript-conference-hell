import asyncio
import unittest
from unittest import mock

import lines


class TestFoo(unittest.IsolatedAsyncioTestCase):

    async def test_add_request_one(self):
        socket = mock.Mock()
        client = lines.Client(socket)
        await client.start()
        client.add_request("foo")
        response = await client.receive_response()
        client.stop()
        self.assertEqual(response, "foo")

if __name__ == '__main__':
    unittest.main()
