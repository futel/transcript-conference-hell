import asyncio
import unittest
from unittest import mock

import speech


class TestFoo(unittest.IsolatedAsyncioTestCase):

    @mock.patch.object(
        speech, 'texttospeech_v1', new_callable=mock.Mock)
    async def test_add_request_one(self, mock_texttospeech_v1):
        client = mock.Mock()
        mock_texttospeech_v1.TextToSpeechAsyncClient = mock.Mock(
            return_value=client)
        speech_client = speech.Client()
        await speech_client.start()
        speech_client.add_request({'text': "foo"})
        speech_client.stop()
        response = await anext(speech_client.request_generator())


if __name__ == '__main__':
    unittest.main()
