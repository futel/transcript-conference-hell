#!/usr/bin/env python3

import sys
sys.path.append('src')

import asyncio

import dotenv
dotenv.load_dotenv()

import chat

lines = open("lines", 'r').readlines()

poetry_lines = [
    "Franz: Are we ready?",
    "xyzzy: Let's begin, I will start.",
    "xyzzy: I shot an arrrow in the air.",
    "Franz: It fell to Earth I know not where."]

#There once was a man from Nantucket.
#Who's head was stuck in a bucket.

async def add_poetry_line():
    line = await chat.rhyming_line(poetry_lines)
    poetry_lines.append("Franz: {}".format(line))
    print(line)

async def main():
    print(await chat.chat_line(lines))
    for i in range(5):
        await add_poetry_line()
    print(poetry_lines)
    print(await chat.rhyme_detector_line(poetry_lines))

asyncio.run(main())
