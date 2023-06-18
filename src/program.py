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

    async def bot_line_or_none(self, population, transcript_lines):
        """
        Return a chat line or None.
        """
        if self.should_bot_line(transcript_lines):
            return await self.bot_line(population, transcript_lines)
        return None


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

    async def has_rhyme(self, transcript_lines):
        """
        Return True if there have been at least two consecutive rhymes
        among the last three lines.
        """
        # There is also the pronouncing library and NLTK for this.
        rhyme_lines = transcript_lines[-2:]
        if len(rhyme_lines) == 2:
            if await chat.rhyme_detector(rhyme_lines):
                return True
                rhyme_lines = transcript_lines[-3:-1]
                if len(rhyme_lines) == 2:
                    if await chat.rhyme_detector(rhyme_lines):
                        return True
        return False

    async def bot_line_or_none(self, population, transcript_lines):
        if False:
            # XXX detect "the end" here
            # XXX validate poem and do outcome
            # XXX can we get away with no state changes victory/defeat?
            # XXX just whatever we say here?
            pass
            return
        elif not self.should_bot_line(transcript_lines):
            return None
        elif await self.has_rhyme(transcript_lines):
            if True:             # XXX half chance
                return await chat.openai_rhyming_line(transcript_lines)
        else:
            # We don't have a rhyme in the last 3 lines.
            return chat.poetry_fail_string()

    def should_bot_line(self, transcript_lines):
        """
        Return True if the bot should reply to a prompt and maybe talk.
        """
        if self.recent_bot_line(transcript_lines):
            return False
        return True
