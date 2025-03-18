#!/usr/bin/env python

"""
The top module executed by the service. Starts the server and runs forever.
"""

import asyncio
import functools
import os

import util
import websocketserver


async def main():
    util.log("server starting")
    util.cred_kluge()

    websocket = websocketserver.Server()
    await websocket.start()
    await asyncio.Future()  # run forever

asyncio.run(main())
