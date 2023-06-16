import asyncio
import unittest
from unittest import mock

import chat

class TestChat(unittest.IsolatedAsyncioTestCase):

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


if __name__ == '__main__':
    unittest.main()
