"""
Download all transcripts from the S3 bucket.
"""
# We don't have real packages.
import sys
sys.path.append('../src')

import asyncio
import dotenv
import os
from unittest import mock

import lines

dotenv.load_dotenv('../.env')
# I don't know why this is needed, but openai doesn't get the env var.
import openai
openai.api_key = os.environ['OPENAI_API_KEY']

#@mock.patch.object(
#        lines, 'util', new_callable=mock.Mock)

async def test():
    socket = mock.Mock()
    socket.attrs = {'bot': True}
    socket.stream_sid = "stream_sid"
    client = lines.Client(socket)
    await client.start()
    client.add_request({'text': "hello"})
    response = await client.receive_response()
    client.stop()
    print(response)

asyncio.run(test())
