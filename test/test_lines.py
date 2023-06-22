import asyncio
import unittest
from unittest import mock

import lines


class TestLines(unittest.IsolatedAsyncioTestCase):

    async def test_str(self):
        line = lines.Line("label", "content")
        self.assertEqual(
            str(line),
            '{"label": "label", "content": "content", "ordinal": null}')
        line = lines.Line("label", "content", foo="foo")
        self.assertEqual(
            str(line),
            '{"label": "label", "content": "content", "ordinal": null, "foo": "foo"}')

class TestClient(unittest.IsolatedAsyncioTestCase):

    async def test_line_from_str(self):
        l = lines.Line("label", "content")
        self.assertEqual(str(lines.line_from_str(str(l))), str(l))

    async def test_line_from_str_bot(self):
        s = """{"label": "Franz", "content": "We don't have enough people.", "ordinal": null, "bot": true}"""
        l = lines.line_from_str(s)
        self.assertTrue(hasattr(l, "bot"))

    @mock.patch.object(
        lines, 'util', new_callable=mock.Mock)
    async def test_client_add_request_one(self, mock_util):
        socket = mock.Mock()
        socket.stream_sid = "stream_sid"
        client = lines.Client(socket)
        await client.start()
        client.add_request({'text': "foo"})
        response = await client.receive_response()
        client.stop()
        self.assertEqual(response, {'text': "foo"})


if __name__ == '__main__':
    unittest.main()
