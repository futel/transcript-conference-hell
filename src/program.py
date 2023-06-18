import itertools
import random

import chat


class Program:
    """
    Holds methods and attributes relevant to bot interaction and
    pipelines for bots and humans.
    """

    async def bot_line(self, population, transcript_lines):
        """Return a line from the bot."""
        raise NotImplementedError

    def recent_bot_line(self, transcript_lines):
        """
        Return True if there aren't yet enough bot lines, or
        the bot has a recent line, in transcript_lines.
        """
        labels = [line.label for line in transcript_lines]
        try:
            for label in [labels.pop(), labels.pop()]:
                if label == chat.chat_label:
                    # One of the last two lines are bot lines.
                    return True
        except IndexError:
            return True
        return False

    def should_bot_line(self, transcript_lines):
        """Return True if the bot should talk."""
        if self.recent_bot_line(transcript_lines):
            return False
        # Half chance of bot line.
        if random.choice([True, False]):
            return True
        return False

    async def bot_lines(self, population, transcript_lines):
        """
        Return a list of zero or more chat lines.
        """
        if self.should_bot_line(transcript_lines):
            return [await self.bot_line(population, transcript_lines)]
        return []


class ChatProgram(Program):
    """
    Chats with humans.
    """
    async def bot_line(self, population, transcript_lines):
        """Return a line from the bot."""
        if population < min_population:
            # Half chance of nagging.
            if random.choice([True, False]):
                return chat.nag_string()
        # We didn't nag, return a chat line.
        return await chat.openai_chat_line(transcript_lines)


class PoetryProgram(Program):
    """
    Recites poetry with humans.
    """
    def __init__(self):
        self.poem_start = None

    async def latest_rhyme(self, t_lines):
        """
        Return the most recent consecutive rhyming lines, or None
        """
        # There is also the pronouncing library and NLTK for this.
        #max_count = 3
        t_lines = reversed(t_lines)
        counter = itertools.count()
        try:
            previous = next(t_lines)
            this = next(t_lines)
            count = next(counter)
            while True: #count < max_count:
                if await chat.rhyme_detector(
                        chat.last_word(this.content),
                        chat.last_word(previous.content)):
                    return (this, previous)
                previous = this
                this = next(t_lines)
                count = next(counter)
        except StopIteration:
            return None

    # async def poem_lines(self, poem_start, poem_end):
    #     poem_end = await self.latest_rhyme(t_lines)
    #     if poem_end is not None:
    #         if poem_start is not None:
    #             # We have a poem going.
    #             # The poem may be continuing, or it may have ended a line ago.
    #             return t_lines[poem_start:-poem_end]
    #         else:
    #             # This is the first rhyme.
    #             return t_lines[-poem_end-1:-poem_end]
    #     return []               # We don't have a poem going.

    async def bot_lines(self, population, t_lines):
        latest_rhyme = await self.latest_rhyme(t_lines)
        if self.poem_start is None:
            if latest_rhyme is None:
                return ["nag"]
            self.poem_start = latest_rhyme[0].ordinal
            #print("xxx poem start", self.poem_start)
            return ["starting"]
        # XXX We should have detected a rhyme, since we did earlier. But we might
        #     need to try again, because chatgpt.
        if latest_rhyme[1].ordinal < len(t_lines) - 2:
            # There have been no rhymes for 2 lines.
            #print('xxx poem', self.poem_start, latest_rhyme[1].ordinal)
            return ["ended"]
        #print('xxx poem', self.poem_start, latest_rhyme[1].ordinal)
        return ["continuing"]

        # latest_rhyme = await self.latest_rhyme(t_lines)
        # print("xxx latest_rhyme", latest_rhyme)
        # if self.poem_start is not None:
        #     print("xxx poem_start", self.poem_start)
        #     # We have a poem going.
        #     if latest_rhyme is not None:
        #         if True:             # XXX make this half chance or less
        #             return await chat.openai_rhyming_line(t_lines)
        #         return []       # Human's turn to talk.
        #     else:
        #         # We don't have a rhyme in the last 3 lines, and we did
        #         # before, so the last line doesn't rhyme.
        #         poem = t_lines[self.poem_start:-latest_rhyme]
        #         print("xxx poem", poem)
        #         self.poem_start = None
        #         if len(poem) > 3:
        #             out = [chat.poetry_success_string()]
        #             out.extend(poem)
        #             return out
        #         return [chat.poetry_fail_string()]
        # # We don't have a poem going.
        # if latest_rhyme is not None:
        #     self.poem_start = len(t_lines) - latest_rhyme
        #     return []
        # # Prompt the human to start a poem.
        # return [chat.poetry_fail_string()]

    def should_bot_line(self, transcript_lines):
        """
        Return True if the bot should reply to a prompt and maybe talk.
        """
        if self.recent_bot_line(transcript_lines):
            return False
        return True
