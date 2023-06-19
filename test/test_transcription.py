import asyncio
import unittest
from unittest import mock

import transcription

class TestStringMethods(unittest.IsolatedAsyncioTestCase):

    async def check_audio_generator_empty(self, bridge):
        """Return True if the audio_generator does not produce within a timeout."""
        try:
            await asyncio.wait_for(anext(bridge.audio_generator()), timeout=1.0)
        except asyncio.TimeoutError:
            return True
        else:
            return False

    @mock.patch.object(
        transcription, 'speech_v1', new_callable=mock.AsyncMock)
    async def test_audio_generator_terminated(self, _mock_speech_v1):
        """
        The audio_generator method of a terminated bridge does not
        produce values.
        """
        client = mock.Mock()
        client.streaming_recognize = mock.Mock(
            return_value=asyncio.Future())
        _mock_speech_v1.SpeechAsyncClient = mock.Mock(return_value=client)
        bridge = transcription.Client()
        await bridge.start()
        bridge.stop()
        async for i in bridge.audio_generator():
            self.fail()

    async def test_audio_generator_empty(self):
        """ The audio_generator method of a bridge with no requests does not produce values."""
        bridge = transcription.Client()
        yield bridge.start()
        self.assertTrue(await self.check_audio_generator_empty(bridge))

    @mock.patch.object(
        transcription, 'speech_v1', new_callable=mock.AsyncMock)
    async def test_audio_generator_one(self, _mock_speech_v1):
        """
        The audio_generator method of a bridge with one request produces
        one value.
        """
        client = mock.Mock()
        client.streaming_recognize = mock.Mock(
            return_value=asyncio.Future())
        _mock_speech_v1.SpeechAsyncClient = mock.Mock(return_value=client)
        in_val = 1
        bridge = transcription.Client()
        await bridge.start()
        bridge.add_request({'chunk': in_val})
        out_val = await anext(bridge.audio_generator())
        self.assertEqual(bytes(in_val), out_val)
        self.assertTrue(await self.check_audio_generator_empty(bridge))

    @mock.patch.object(
        transcription, 'speech_v1', new_callable=mock.AsyncMock)
    async def test_audio_generator_two(self, _mock_speech_v1):
        """
        The audio_generator method of a bridge with two requests
        produces one value.
        """
        client = mock.Mock()
        client.streaming_recognize = mock.Mock(
            return_value=asyncio.Future())
        _mock_speech_v1.SpeechAsyncClient = mock.Mock(return_value=client)
        in_vals = [1, 2]
        bridge = transcription.Client()
        await bridge.start()
        for i in in_vals:
            bridge.add_request({'chunk': i})
        out_val = await anext(bridge.audio_generator())
        self.assertEqual(b"".join(bytes(i) for i in in_vals), out_val)
        self.assertTrue(await self.check_audio_generator_empty(bridge))


if __name__ == '__main__':
    unittest.main()
