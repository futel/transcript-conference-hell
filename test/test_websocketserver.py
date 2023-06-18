import asyncio
import unittest
from unittest import mock

import program


class TestProgram(unittest.IsolatedAsyncioTestCase):

    async def test_bot_lines(self):
        prog = program.Program()
        self.assertEqual(await prog.bot_lines(666, []), [])


class TestPoetryProgram(unittest.IsolatedAsyncioTestCase):

    async def test_bot_lines(self):
        prog = program.PoetryProgram()
        bot_lines = await prog.bot_lines(666, [])
        self.assertTrue(isinstance(bot_lines.pop(), str))

    async def test_latest_rhyme(self):
        prog = program.PoetryProgram()
        self.assertEqual(await prog.latest_rhyme([]), None)


if __name__ == '__main__':
    unittest.main()
