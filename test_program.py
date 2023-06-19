#!/usr/bin/env python3

import sys
sys.path.append('src')

import asyncio

import dotenv
dotenv.load_dotenv()

import lines
import program

poetry_lines_zero = [
    lines.Line("Franz", "Are we ready?"),
    lines.Line("xyzzy", "Let's begin, I will start."),
    lines.Line("xyzzy", "I shot an arrrow in the air."),
    lines.Line("foobar", "It fell to Earth I know not where.")]

poetry_lines_two = [
    lines.Line("Franz", "Are we ready?"),
    lines.Line("xyzzy", "Let's begin, I will start."),
    lines.Line("xyzzy", "I shot an arrrow in the air."),
    lines.Line("xyzzy", "It fell to Earth I know not where."),
    lines.Line("xyzzy", "But when I heard a distant sound"),
    lines.Line("xyzzy", "I knew the arrow had been found."),
    lines.Line("xyzzy", "It fell to Earth I know not where."),
    lines.Line("foobar", "It fell to Earth hello hello."),
    lines.Line("foobar", "It fell to Earth goodbye.")]

poetry_lines_none = [
    lines.Line("Franz", "Are we ready?"),
    lines.Line("xyzzy", "Let's begin, I will start."),
    lines.Line("xyzzy", "I shot an arrrow in the air."),
    lines.Line("foobar", "It fell to Earth hello hello.")]

poetry_lines_foo = [
    lines.Line("Franz", "Yesterday, upon the stair,"),
    lines.Line("Franz", "I met a man who wasn't there!"),
    lines.Line("Franz", "He wasn't there again today,"),
    lines.Line("Franz", "Oh how I wish he'd go away!"),
    lines.Line("Franz", "When I came home last night at three,"),
    lines.Line("Franz", "The man was waiting there for me"),
    lines.Line("Franz", "But when I looked around the hall,"),
    lines.Line("Franz", "I couldn't see him there at all!")]

# async def add_poetry_line():
#     line = await chat.rhyming_line(poetry_lines)
#     poetry_lines.append("Franz: {}".format(line))
#     print(line)

async def main():
    prog = program.PoetryProgram()
    # print(await prog.latest_rhyme(poetry_lines_zero))
    # print(await prog.latest_rhyme(poetry_lines_two))
    # print(await prog.latest_rhyme(poetry_lines_none))

    for poem in [
            #poetry_lines_zero,
            #poetry_lines_two,
            #poetry_lines_none,
            poetry_lines_foo
    ]:
        print("new poem")
        prog = program.PoetryProgram()
        for latest in range(len(poem)+1):
            print(poem[0:latest])
            print(await prog.bot_lines(666, poem[0:latest]))
            print

    #print(await prog.bot_lines(666, poetry_lines_none)) # continuing


asyncio.run(main())
