#!/usr/bin/env python3

import sys
sys.path.append('src')

import asyncio

import dotenv
dotenv.load_dotenv()

import chat
import lines

t_lines = open("lines", 'r').readlines()

poetry_lines = [
    lines.line_from_str(s) for s in [
        "Franz: Are we ready?",
        "xyzzy: Let's begin, I will start.",
        "xyzzy: I shot an arrrow in the air.",
        "Franz: It fell to Earth I know not where."]]

#There once was a man from Nantucket.
#Who's head was stuck in a bucket.

async def add_poetry_line():
    line = await chat.openai_rhyming_line(poetry_lines)
    poetry_lines.append(lines.Line("Franz", line))
    print(line)

async def main():
    print(await chat.rhyme_detector("dog", "frog"))
    print(await chat.rhyme_detector("giggle", "wiggle"))
    print(await chat.rhyme_detector("cringe", "impinge"))
    print(await chat.rhyme_detector("air", "where"))
    print(await chat.rhyme_detector("where", "sound"))
    print(await chat.rhyme_detector("three", "me"))
    print(await chat.rhyme_detector("sound", "found"))

    # for i in range(5):
    #     await add_poetry_line()

asyncio.run(main())
