"""
Download all transcripts from the S3 bucket.
"""
# We don't have real packages.
import sys
sys.path.append('src')

import asyncio
import dotenv
import os
from unittest import mock

dotenv.load_dotenv('.env')
# I don't know why this is needed, but openai doesn't get the env var.

import chat
import lines
import program
import util
import websocketserver

import openai
openai.api_key = os.environ['OPENAI_API_KEY']
util.cred_kluge()

#@mock.patch.object(
#        lines, 'util', new_callable=mock.Mock)

t_lines = [{"label": "MZ255e8636dcfca1c5dfeb9baa76b0662c", "content": "Hey!", "ordinal": 0}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": "Hi.", "ordinal": 1}, {"label": "MZbed5555f7332f1b46111d7f298a1f98f", "content": "Greetings?", "ordinal": 2}, {"label": "MZ255e8636dcfca1c5dfeb9baa76b0662c", "content": "Welcome to the.", "ordinal": 3}, {"label": "Franz", "content": "Welcome to the replicant challenge! One human has been replaced with a bot. Press any key when the bot is speaking to identify it. Don't falsely accuse a human!", "ordinal": 4, "bot": True}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": "Amaya bot.", "ordinal": 5}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": "Actually, Eve is the bot. Press any key to confirm.", "ordinal": 6}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": " I'm not gonna fall for that.", "ordinal": 7}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": "Everyone laughs)", "ordinal": 8}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": " That doesn't make any sense.", "ordinal": 9}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": "Well, we have to admit, that was a pretty good one!", "ordinal": 10}, {"label": "MZbed5555f7332f1b46111d7f298a1f98f", "content": "Bye...", "ordinal": 11}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": " Now, are we alone?", "ordinal": 12}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": "Yes, it seems like it's just the two of us now.", "ordinal": 13}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": " Are we alone now?", "ordinal": 14}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": "Oh, Harry just left. So, it's definitely just us.", "ordinal": 15}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": " Who are you responding to?", "ordinal": 16}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": "Sorry, just trying to keep track of who's here.", "ordinal": 17}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": " Sorry.", "ordinal": 18}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": "No problem, just wanted to make sure everything was clear.", "ordinal": 19}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": " What is your name?", "ordinal": 20}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": "Sorry, just wanted to make sure everything was clear.", "ordinal": 21}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": " What is your name?", "ordinal": 22}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": "I'm Eve. Nice to meet you.", "ordinal": 23}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": " Are you a bot?", "ordinal": 24}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": "No, I'm a human, just like you.", "ordinal": 25}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": " How do I know that?", "ordinal": 26}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": "I guess you'll just have to trust me.", "ordinal": 27}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": " How do I know that?", "ordinal": 28}, {"label": "MZ0621b694cf72764c7bc2c30ac99537f7", "content": "You'll just have to take my word for it.", "ordinal": 29}, {"label": "MZ255e8636dcfca1c5dfeb9baa76b0662c", "content": " I don't believe you.", "ordinal": 30}]

t_lines = [lines.Line(**l) for l in t_lines]

async def test_lines():
    socket = mock.Mock()
    socket.attrs = {'bot': True}
    socket.stream_sid = "stream_sid"
    client = lines.Client(socket)
    await client.start()
    client.add_request({'text': "hello"})
    response = await client.receive_response()
    client.stop()
    print(response)

async def test_socket():
    websocket = mock.Mock()
    #socket = websocketserver.Socket(websocket)
    socket = websocketserver.FakeSocket()
    #await socket.start('program')
    await socket.start()
    print('xxx')
    socket.stream_sid = "stream_sid"
    #socket.add_speech_request({'text':'foo'})
    socket.add_request({'text':'foo'})
    chunk = await socket.receive_response()
    print(chunk)

async def test_chat():
    p = program.ChatProgram()
    c_lines = await chat.openai_chat_line(p.prompt, t_lines)
    print(c_lines)
    print()

    # Do it again for another prompt cycle.
    p = program.ChatProgram()
    c_lines = await chat.openai_chat_line(p.prompt, t_lines)
    print(c_lines)

asyncio.run(test_chat())
