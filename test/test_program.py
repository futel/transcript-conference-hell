import asyncio
import unittest
from unittest import mock

import lines
import program
import websocketserver


class TestProgram(unittest.IsolatedAsyncioTestCase):

    def test_next_program(self):
        program_cycle = program.next_program()
        self.assertEqual(next(program_cycle), program.ReplicantProgram)
        self.assertEqual(next(program_cycle), program.ChatProgram)

    async def test_recent_bot_line(self):
        prog = program.Program()
        t_lines = []
        self.assertEqual(prog.recent_bot_line(2, t_lines), True)
        t_lines.append(lines.Line('label', 'content'))
        self.assertEqual(prog.recent_bot_line(2, t_lines), False)
        t_lines.append(lines.Line('label', 'content'))
        self.assertEqual(prog.recent_bot_line(2, t_lines), False)
        t_lines.append(lines.Line('label', 'content'))
        t_lines.append(lines.Line('label', 'content'))
        t_lines.append(lines.Line('label', 'content'))
        t_lines.append(lines.Line('label', 'content'))
        t_lines.append(lines.Line('label', 'content'))
        t_lines.append(lines.Line('label', 'content'))
        self.assertEqual(prog.recent_bot_line(2, t_lines), False)
        t_lines.append(lines.Line('label', 'content', silent=True))
        self.assertEqual(prog.recent_bot_line(2, t_lines), False)
        t_lines.append(lines.Line('label', 'content', bot=True))
        self.assertEqual(prog.recent_bot_line(2, t_lines), True)
        t_lines.append(lines.Line('label', 'content'))
        self.assertEqual(prog.recent_bot_line(2, t_lines), False)
        t_lines.append(lines.Line('label', 'content'))
        self.assertEqual(prog.recent_bot_line(2, t_lines), False)
        t_lines.append(lines.Line('label', 'content'))
        self.assertEqual(prog.recent_bot_line(2, t_lines), False)
        t_lines.append(lines.Line('label', 'content'))
        t_lines.append(lines.Line('label', 'content'))
        t_lines.append(lines.Line('label', 'content'))
        t_lines.append(lines.Line('label', 'content'))
        t_lines.append(lines.Line('label', 'content'))
        t_lines.append(lines.Line('label', 'content'))
        self.assertEqual(prog.recent_bot_line(2, t_lines), False)

    def test_handle_dtmf(self):
        prog = program.Program()
        self.assertEqual(prog.handle_dtmf({}, 'socket', 'latest_socket', 1), [])

class TestArithmeticProgram(unittest.IsolatedAsyncioTestCase):

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

    async def test_bot_lines_false(self):
        prog = program.ArithmeticProgram()
        l = [
            lines.Line('label', "foo bar baz"),
            lines.Line('label', "foo bar baz"),
            lines.Line('label', "foo bar baz"),
            lines.Line('label', "foo bar baz"),
            lines.Line('label', "foo bar baz")]
        self.assertEqual(
            await prog.bot_lines(0, [], 'dummy'), [])
        self.assertEqual(
            await prog.bot_lines(1, [], 'dummy'), [])
        self.assertEqual(
            await prog.bot_lines(2, [], 'dummy'), [])

    def test_intro_text(self):
        socket = mock.Mock()
        socket.stream_sid = "abc1d23ef4g"
        prog = program.ArithmeticProgram()
        self.assertEqual(
            prog.intro_text(socket, "population"),
            "Welcome to the arithmetic challenge! Each human has an integer. To succeed, state the sum of all the integers.Your integer is 4.")


class TestReplicantProgram(unittest.IsolatedAsyncioTestCase):

    def test_handle_dtmf(self):
        prog = program.ReplicantProgram()
        socket = websocketserver.Socket('websocket')
        self.assertTrue(
            prog.handle_dtmf({}, 'socket', 'latest_socket', [socket]))
        self.assertTrue(
            prog.handle_dtmf(
                {}, 'socket', 'latest_socket', [socket, socket, socket]))


if __name__ == '__main__':
    unittest.main()
