import asyncio
import unittest
from unittest import mock

import lines
import program


class TestProgram(unittest.IsolatedAsyncioTestCase):

    async def test_recent_bot_line(self):
        prog = program.Program()
        t_lines = [
            lines.Line('label', 'content'),
            lines.Line('label', 'content')]
        self.assertEqual(prog.recent_bot_line(t_lines), False)
        t_lines.append(lines.Line('label', 'content', silent=True))
        self.assertEqual(prog.recent_bot_line(t_lines), False)
        t_lines.append(lines.Line('label', 'content', bot=True))
        self.assertEqual(prog.recent_bot_line(t_lines), True)
        t_lines.append(lines.Line('label', 'content'))
        self.assertEqual(prog.recent_bot_line(t_lines), True)
        t_lines.append(lines.Line('label', 'content'))
        self.assertEqual(prog.recent_bot_line(t_lines), False)


if __name__ == '__main__':
    unittest.main()
