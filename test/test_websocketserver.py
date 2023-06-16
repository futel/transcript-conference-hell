import asyncio
import unittest
from unittest import mock

import websocketserver


class TestProgram(unittest.IsolatedAsyncioTestCase):

    async def test_bot_line_or_none_none(self):
        program = websocketserver.Program()
        self.assertEqual(await program.bot_line_or_none(666, []), None)


class TestPoetryProgram(unittest.IsolatedAsyncioTestCase):

    async def test_bot_line_or_none_none(self):
        program = websocketserver.PoetryProgram()
        self.assertEqual(await program.bot_line_or_none(666, []), None)

    async def test_has_rhyme(self):
        program = websocketserver.PoetryProgram()
        self.assertEqual(await program.has_rhyme([]), False)


if __name__ == '__main__':
    unittest.main()
