#!/usr/bin/env python3

import sys
sys.path.append('src')

import asyncio

import dotenv
dotenv.load_dotenv()

import chat
import lines

#t_lines = open("lines", 'r').readlines()

poetry_lines = [
    lines.Line("Franz", "Are we ready?"),
    lines.Line("xyzzy", "Let's begin, I will start."),
    lines.Line("xyzzy", "I shot an arrrow in the air."),
    lines.Line("Franz", "It fell to Earth I know not where.")]

t_lines = [
    lines.Line("Franz", "Are we ready?"),
    lines.Line("xyzzy", "Let's begin, I will start."),
    lines.Line("xyzzy", "My name is Bob, what is yours?"),
    lines.Line("Franz", "My name is Franz."),
    lines.Line("ab234", "I don't want to tell you my name.")]

#There once was a man from Nantucket.
#Who's head was stuck in a bucket.

async def add_poetry_line():
    line = await chat.openai_rhyming_line(poetry_lines)
    poetry_lines.append(lines.Line("Franz", line))
    print(line)

async def add_chat_line():
    line = await chat.openai_chat_line(t_lines)
    t_lines.append(lines.Line("Franz", line))
    print(line)

async def main():
    for i in range(5):
        await add_chat_line()

    print(await chat.rhyme_detector("dog", "frog"))
    print(await chat.rhyme_detector("giggle", "wiggle"))
    print(await chat.rhyme_detector("cringe", "impinge"))
    print(await chat.rhyme_detector("air", "where"))
    print(await chat.rhyme_detector("where", "sound"))
    print(await chat.rhyme_detector("three", "me"))
    print(await chat.rhyme_detector("sound", "found"))


asyncio.run(main())
