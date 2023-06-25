#!/usr/bin/env python3

import sys
sys.path.append('src')

import asyncio

import dotenv
dotenv.load_dotenv()

import pipeline
import chat
import lines
import speech
import util
import websocketserver

util.cred_kluge()

sock = websocketserver.Socket('dummy')
sock.stream_sid = 'stream_sid'

async def note_response(l):
    response = await l.receive_response()
    print('response')

async def r_response(l):
    while True:
        await note_response(l)

async def main():
    l = pipeline.HumanPipeline(sock)
    await l.start()
    #asyncio.create_task(r_response(l))
    l.line_speech_line.add_request({'text': 'text'})
    l.line_speech_line.add_request({'text': 'text'})

    await note_response(l)
    print('response')
    await note_response(l)
    print('response')

    l.stop()
    await l.start()

    await note_response(l)
    print('response')
    await note_response(l)
    print('response')

    await asyncio.Future()

asyncio.run(main())
