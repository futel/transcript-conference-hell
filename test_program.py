#!/usr/bin/env python3

import sys
sys.path.append('src')

import asyncio

import dotenv
dotenv.load_dotenv()

import websocketserver

poetry_lines = [
    "Franz: Are we ready?",
    "xyzzy: Let's begin, I will start.",
    "xyzzy: I shot an arrrow in the air.",
    "Franz: It fell to Earth I know not where."]

# async def add_poetry_line():
#     line = await chat.rhyming_line(poetry_lines)
#     poetry_lines.append("Franz: {}".format(line))
#     print(line)

async def main():
    program = websocketserver.PoetryProgram()
    #print(await program.has_rhyme(poetry_lines))
    print(await program.bot_line_or_none(666, poetry_lines))


asyncio.run(main())
