#!/usr/bin/env python

import asyncio
import functools
import os

import util
import websocketserver

# def save_chunk(chunk):
#     # testing
#     now = time.time()
#     filename = f"chunk{now}"
#     with open(filename, "ab") as f:
#         f.write(chunk)

async def main():
    util.log("server starting")
    util.cred_kluge()

    websocket = websocketserver.Server()
    await websocket.start()
    await asyncio.Future()  # run forever

asyncio.run(main())
