import asyncio
import unittest
from unittest import mock

import lines
import program


class TestProgram(unittest.IsolatedAsyncioTestCase):

    def test_next_program(self):
        program_cycle = program.next_program()
        self.assertEqual(next(program_cycle), program.ChatProgram)
        self.assertEqual(next(program_cycle), program.ArithmeticProgram)

    async def test_recent_bot_line(self):
        prog = program.Program()
        t_lines = [
            lines.Line('label', 'content'),
            lines.Line('label', 'content')]
        self.assertEqual(prog.recent_bot_line(t_lines), True)
        t_lines.append(lines.Line('label', 'content'))
        t_lines.append(lines.Line('label', 'content'))
        t_lines.append(lines.Line('label', 'content'))
        t_lines.append(lines.Line('label', 'content'))
        t_lines.append(lines.Line('label', 'content'))
        self.assertEqual(prog.recent_bot_line(t_lines), False)
        t_lines.append(lines.Line('label', 'content', silent=True))
        self.assertEqual(prog.recent_bot_line(t_lines), False)
        t_lines.append(lines.Line('label', 'content', bot=True))
        self.assertEqual(prog.recent_bot_line(t_lines), True)
        t_lines.append(lines.Line('label', 'content'))
        self.assertEqual(prog.recent_bot_line(t_lines), True)
        t_lines.append(lines.Line('label', 'content'))
        self.assertEqual(prog.recent_bot_line(t_lines), True)
        t_lines.append(lines.Line('label', 'content'))
        self.assertEqual(prog.recent_bot_line(t_lines), False)

class TestArithmeticProgram(unittest.IsolatedAsyncioTestCase):

    def test_recent_bot_line(self):
        prog = program.ArithmeticProgram()
        t_lines = []
        self.assertEqual(prog.recent_bot_line(t_lines), True)
        t_lines.append(lines.Line('label', 'content'))
        self.assertEqual(prog.recent_bot_line(t_lines), False)
        self.assertEqual(prog.recent_bot_line(t_lines), False)
        t_lines.append(lines.Line('label', 'content', silent=True))
        self.assertEqual(prog.recent_bot_line(t_lines), False)
        t_lines.append(lines.Line('label', 'content', bot=True))
        self.assertEqual(prog.recent_bot_line(t_lines), True)
        t_lines.append(lines.Line('label', 'content'))
        self.assertEqual(prog.recent_bot_line(t_lines), False)
        t_lines.append(lines.Line('label', 'content'))
        self.assertEqual(prog.recent_bot_line(t_lines), False)

    def test_word_to_integer(self):
        self.assertEqual(program.ArithmeticProgram().word_to_integer("seven"), 7)

    def test_line_to_integer(self):
        prog = program.ArithmeticProgram()
        self.assertEqual(prog.line_to_integer(
            lines.Line('label', "7")), 7)
        self.assertEqual(prog.line_to_integer(
            lines.Line('label', "seven")), 7)
        self.assertEqual(prog.line_to_integer(
            lines.Line('label', "six seven")), 67)
        self.assertEqual(prog.line_to_integer(
            lines.Line('label', "three six seven")), 367)
        self.assertEqual(prog.line_to_integer(
            lines.Line('label', "foo bar baz")), None)

    def test_recent_ints(self):
        prog = program.ArithmeticProgram()
        self.assertEqual(prog.recent_ints([]), [])
        self.assertEqual(prog.recent_ints([lines.Line('label', "foo")]), [])
        self.assertEqual(prog.recent_ints([lines.Line('label', "1")]), [1])
        self.assertEqual(prog.recent_ints(
            [lines.Line('label', "foo 0 bar")]), [0])
        self.assertEqual(prog.recent_ints(
            [lines.Line('label', "foo 1 bar")]), [1])
        self.assertEqual(prog.recent_ints(
            [lines.Line('label', "1"),
             lines.Line('label', "0"),
             lines.Line('label', "2")]), [2, 0, 1])

    def test_intro_text(self):
        socket = mock.Mock()
        socket.stream_sid = "abc1d23ef4g"
        prog = program.ArithmeticProgram()
        self.assertEqual(
            prog.intro_text(socket),
            "Welcome to the arithmetic challenge! Each human has an integer. To succeed, state the sum of all the integers.Your integer is 4.")


if __name__ == '__main__':
    unittest.main()
