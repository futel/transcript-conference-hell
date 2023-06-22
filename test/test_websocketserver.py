import asyncio
import unittest
from unittest import mock

import program


class TestPoetryProgram(unittest.IsolatedAsyncioTestCase):

    async def test_bot_lines(self):
        prog = program.PoetryProgram()
        bot_lines = await prog.bot_lines(666, [], 'dummy')
        self.assertEqual(bot_lines, [])

    async def test_latest_rhyme(self):
        prog = program.PoetryProgram()
        self.assertEqual(await prog.latest_rhyme([]), None)


if __name__ == '__main__':
    unittest.main()
