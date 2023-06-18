import asyncio
import unittest
from unittest import mock

import program


class TestProgram(unittest.IsolatedAsyncioTestCase):

    async def test_bot_line_or_none_none(self):
        prog = program.Program()
        self.assertEqual(await prog.bot_line_or_none(666, []), None)


class TestPoetryProgram(unittest.IsolatedAsyncioTestCase):

    async def test_bot_line_or_none_none(self):
        prog = program.PoetryProgram()
        self.assertEqual(await prog.bot_line_or_none(666, []), None)

    async def test_has_rhyme(self):
        prog = program.PoetryProgram()
        self.assertEqual(await prog.has_rhyme([]), False)


if __name__ == '__main__':
    unittest.main()
