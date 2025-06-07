import asyncio
import unittest
from unittest import mock

import chat

class TestChat(unittest.IsolatedAsyncioTestCase):

    def test_next_prompt(self):
        prompt_cycle = chat.next_prompt()
        p1 = next(prompt_cycle)
        dummy1 = next(prompt_cycle)
        #dummy2 = next(prompt_cycle)
        p2 = next(prompt_cycle)
        self.assertNotEqual(p1, dummy1)
        #self.assertNotEqual(p1, dummy2)
        self.assertEqual(p1, p2)

    def test_line_to_bool(self):
        self.assertEqual(chat.line_to_bool("True"), True)
        self.assertEqual(chat.line_to_bool("False"), False)
        self.assertEqual(chat.line_to_bool("true"), True)
        self.assertEqual(chat.line_to_bool("false"), False)
        self.assertEqual(chat.line_to_bool("True."), True)
        self.assertEqual(chat.line_to_bool("False."), False)
        self.assertEqual(chat.line_to_bool(" True. "), True)
        self.assertEqual(chat.line_to_bool(" False. "), False)
        self.assertEqual(
            chat.line_to_bool(" True. Another sentence. "), True)
        self.assertEqual(
            chat.line_to_bool(" False. Another sentence. "), False)

    def test_last_word(self):
        self.assertEqual(chat.last_word("True"), "true")
        self.assertEqual(chat.last_word(" Foo Bar False."), "false")
        self.assertEqual(chat.last_word(" Foo "), "foo")


if __name__ == '__main__':
    unittest.main()
