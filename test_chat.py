#!/usr/bin/env python3

import asyncio
import dotenv

dotenv.load_dotenv()
import chat

lines = open("lines", 'r').readlines()

async def main():
    print(await chat.chat_line(lines))

asyncio.run(main())
