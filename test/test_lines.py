import asyncio
import unittest
from unittest import mock

import lines


class TestLines(unittest.IsolatedAsyncioTestCase):

    async def test_str(self):
        line = lines.Line("label", "content")
        self.assertEqual(
            str(line), '{"label": "label", "content": "content"}')
        line = lines.Line("label", "content", foo="foo")
        self.assertEqual(
            str(line), '{"label": "label", "content": "content", "foo": "foo"}')

class TestClient(unittest.IsolatedAsyncioTestCase):

    @mock.patch.object(
        lines, 'util', new_callable=mock.Mock)
    async def test_client_add_request_one(self, mock_util):
        socket = mock.Mock()
        socket.stream_sid = "stream_sid"
        client = lines.Client(socket)
        await client.start()
        client.add_request("foo")
        response = await client.receive_response()
        client.stop()
        self.assertEqual(response, "foo")

    @mock.patch.object(
        lines, 'util', new_callable=mock.Mock)
    async def test_replicant_client_add_request_one(self, mock_util):
        socket = mock.Mock()
        socket.stream_sid = "stream_sid"
        client = lines.ReplicantClient(socket, bot=True)
        await client.start()
        client.add_request("foo", "bar")
        response = await client.receive_response()
        client.stop()
        self.assertEqual(response, "bar")


if __name__ == '__main__':
    unittest.main()
