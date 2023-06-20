import itertools
import random

import chat
import pipeline

# Bot may nag humans if population is fewer than this.
nag_population = 2


class Program:
    """
    Holds methods and attributes relevant to bot interaction and
    pipelines for bots and humans.
    """

    def get_pipeline(self, socket):
        """ Return a client pipeline for chunk requests and responses."""
        return pipeline.HumanPipeline(socket)

    async def bot_line(self, population, transcript_lines):
        """Return a line from the bot."""
        raise NotImplementedError

    def recent_bot_line(self, transcript_lines):
        """
        Return True if there aren't yet enough bot lines, or
        the bot has a recent line, in transcript_lines.
        """
        t_lines = [
            l for l in transcript_lines if not hasattr(l, 'silent')]
        try:
            for t_line in [t_lines.pop(), t_lines.pop()]:
                if hasattr(t_line, 'bot'):
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
        if population < nag_population:
            # Half chance of nagging.
            if random.choice([True, False]):
                return chat.nag_string()
        # We didn't nag, return a chat line.
        return await chat.openai_chat_line(transcript_lines)


class ReplicantProgram(ChatProgram):

    def get_pipeline(self, socket):
        return pipeline.ReplicantPipeline(socket)


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

    async def bot_lines(self, population, t_lines):
        latest_rhyme = await self.latest_rhyme(t_lines)
        if self.poem_start is None:
            if latest_rhyme is None:
                if len(t_lines) >= 2:
                    return [chat.poetry_fail_string()]
                return []       # Give the human time.
            self.poem_start = latest_rhyme[0].ordinal
            return []           # Human's turn to talk.
        # XXX We should have detected a rhyme, since we did earlier.
        #     But we might need to try again, because chatgpt.
        if latest_rhyme[1].ordinal < len(t_lines) - 2:
            # There have been no rhymes for 2 lines.
            out = [chat.poetry_succeed_string()]
            out.extend(t_lines[self.poem_start:latest_rhyme[1].ordinal+1])
            return out
        if random.choice([True, False]): # Half chance of bot line.
            return [await chat.openai_rhyming_line(t_lines)]
        return []               # Human's turn to talk.

    def should_bot_line(self, transcript_lines):
        """
        Return True if the bot should reply to a prompt and maybe talk.
        """
        if self.recent_bot_line(transcript_lines):
            return False
        return True


class PoetryAppreciatorProgram(PoetryProgram):
    """
    Appreciates poetry when found.
    """
    async def bot_lines(self, population, t_lines):
        latest_rhyme = await self.latest_rhyme(t_lines)
        if self.poem_start is None:
            if latest_rhyme is not None:
                self.poem_start = latest_rhyme[0].ordinal
                return []           # Human's turn to talk.
        # XXX We should have detected a rhyme, since we did earlier.
        #     But we might need to try again, because chatgpt.
        if latest_rhyme[1].ordinal < len(t_lines) - 2:
            # There have been no rhymes for 2 lines.
            out = [chat.poetry_succeed_string()]
            out.extend(t_lines[self.poem_start:latest_rhyme[1].ordinal+1])
            return out
        return []               # Human's turn to talk.

