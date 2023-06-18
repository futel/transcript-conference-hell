#!/usr/bin/env python3

import sys
sys.path.append('src')

import asyncio

import dotenv
dotenv.load_dotenv()

import lines
import program

poetry_lines_zero = [
    lines.line_from_str(s, ordinal=idx) for (idx, s) in enumerate([
        "Franz: Are we ready?",
        "xyzzy: Let's begin, I will start.",
        "xyzzy: I shot an arrrow in the air.",
        "foobar: It fell to Earth I know not where."])]

poetry_lines_two = [
    lines.line_from_str(s, ordinal=idx) for (idx, s) in enumerate([
        "Franz: Are we ready?",
        "xyzzy: Let's begin, I will start.",
        "xyzzy: I shot an arrrow in the air.",
        "xyzzy: It fell to Earth I know not where.",
        "xyzzy: But when I heard a distant sound",
        "xyzzy: I knew the arrow had been found.",
        "xyzzy: It fell to Earth I know not where.",
        "foobar: It fell to Earth hello hello.",
        "foobar: It fell to Earth goodbye."])]

poetry_lines_none = [
    lines.line_from_str(s, ordinal=idx) for (idx, s) in enumerate([
        "Franz: Are we ready?",
        "xyzzy: Let's begin, I will start.",
        "xyzzy: I shot an arrrow in the air.",
        "foobar: It fell to Earth hello hello."])]

poetry_lines_foo = [
    lines.line_from_str(s, ordinal=idx) for (idx, s) in enumerate([
        "Franz: Yesterday, upon the stair,",
        "Franz: I met a man who wasn't there!",
        "Franz: He wasn't there again today,",
        "Franz: Oh how I wish he'd go away!",
        "Franz: When I came home last night at three,",
        "Franz: The man was waiting there for me",
        "Franz: But when I looked around the hall,",
        "Franz: I couldn't see him there at all!"])]

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
