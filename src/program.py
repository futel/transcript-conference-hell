import itertools
import random

import chat
import pipeline
import util

# Bot may nag humans if population is fewer than this.
nag_population = 2

prompt_cycle = chat.next_prompt()


class Program:
    """
    Holds methods and attributes relevant to bot interaction and
    pipelines for bots and humans.
    """
    intro_string = "Welcome to transcription hell, human!"
    num_human_lines = 3         # Human lines before bot talks.

    def __init__(self):
        util.log('Initializing program {}'.format(
            self.__class__.__name__))
        self.prompt = next(prompt_cycle)
        self.victory = False

    # XXX websocket server needs the line to stay the same
    # def get_pipeline(self, socket):
    #     """
    #     Return a pipeline for chunk requests and responses,
    #     for human clients.
    #     """
    #     return pipeline.HumanPipeline(socket)

    def intro_text(self, socket):
        return self.intro_string

    def nag_line(self, population):
        """Retrn a nag line or None."""
        if population < nag_population:
            # Third chance.
            if random.choice([True, False, False]):
                return chat.nag_string()
        return None

    # async def bot_line(self, population, transcript_lines, server):
    #     """Return a line from the bot."""
    #     raise NotImplementedError

    def recent_bot_line(self, population, transcript_lines):
        """
        Return True if there aren't yet enough bot lines, or
        the bot has a recent line, in transcript_lines.
        """
        t_lines = [
            l for l in transcript_lines if not hasattr(l, 'silent')]
        try:
            num_lines = self.num_human_lines
            if population < 2:
                num_lines = 1
            for x in range(num_lines):
                t_line = t_lines.pop()
                if hasattr(t_line, 'bot'):
                    # One of the recent lines are bot lines.
                    return True
        except IndexError:
            # Not enough lines.
            return True
        return False

    def should_bot_line(self, population, transcript_lines):
        """Return True if the bot should talk."""
        if self.recent_bot_line(population, transcript_lines):
            return False
        # Half chance of bot line.
        if random.choice([True, False]):
            return True
        return False

    # async def bot_lines(self, population, transcript_lines, server):
    #     """
    #     Return a list of zero or more chat lines.
    #     """
    #     if self.should_bot_line(transcript_lines):
    #         bot_line = await self.bot_line(population, transcript_lines, server)
    #         if bot_line:
    #             return [bot_line]
    #     return []


class ChatProgram(Program):
    """
    Chats with humans.
    """
    async def bot_lines(self, population, transcript_lines, server):
        if self.should_bot_line(population, transcript_lines):
            if self.nag_line(population):
                # Half chance of nag line.
                if random.choice([True, False]):
                    return [chat.nag_string()]
            # We didn't nag, return a chat line.
            #util.log('bot returning chat line')
            chat_line = await chat.openai_chat_line(
                self.prompt, transcript_lines)
            if chat_line:
                return [chat_line]
        return []


class ArithmeticProgram(Program):
    intro_string = (
        "Welcome to the arithmetic challenge! "
        "Each human has an integer. "
        "To succeed, state the sum of all the integers.")
    num_human_lines = 1

    def intro_text(self, socket):
        out = "Your integer is {}.".format(
            self.sid_to_integer(socket.stream_sid))
        return self.intro_string + out

    def word_to_integer(self, w):
        """Return the integer corresponding to w, or None."""
        # This doesn't include integers above ten, to do so,
        # we need to do arithmetic.
        if w.isdigit():
            return int(w)
        word_integer = {
            'zero': 0,
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'for': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'ate': 8,
            'nine': 9}
        return word_integer.get(w)

    def line_to_integer(self, l):
        """Return the integer corresponding to l, or None."""
        # In practice we get "1 2 3", but:
        # 123
        # 1 2 3
        # one two three
        # one hundred twenty three
        # one hundred and twenty three
        # plus puncuation
        l = chat.words(l.content)
        # For hundreds, we really need to translate tens and replace
        # missing tens with 0.
        # It should be OK since we don't expect hundreds
        # to be correct, and the speech to text tends to turn them into
        # integers anyway.
        #l = [w for w in l if w not in ['hundred', 'and']]
        l = [self.word_to_integer(w) for w in l]
        l = [w for w in l if w is not None]
        if not l:
            return None
        return sum([w * (10 ** i) for i, w in enumerate(reversed(l))])

    def recent_human_lines(self, transcript_lines):
        """Yield the lines humans have spoken since last bot line."""
        for t_line in reversed(transcript_lines):
            if hasattr(t_line, 'bot'):
                break
            yield t_line

    def magic_integer(self, server):
        """Return the integer we want humans to say."""
        return sum(
            [self.sid_to_integer(socket.stream_sid)
             for socket in server.sockets])

    def sid_to_integer(self, sid):
        """Return the integer corresponding to sid."""
        # MZ58fa2ba422c3b0c73b7e1ebe7f625a14
        return [int(c) for c in sid if c.isdigit()].pop()

    def check_lines(self, ints, magic_integer):
        """
        Return True if magic integer is in ints.
        If another integer is in ints, return one of them.
        """
        for i in ints:
            if i == magic_integer:
                return True
        return ints.pop()

    def recent_ints(self, transcript_lines):
        ints = [self.line_to_integer(h_line)
                for h_line in self.recent_human_lines(transcript_lines)]
        return [i for i in ints if i is not None]

    async def bot_lines(self, population, transcript_lines, server):
        """Return a line from the bot."""
        # Has a human spoken the number since the last bot line?
        # If true, say victory.
        # If false, prompt.
        ints = self.recent_ints(transcript_lines)
        if ints:
            # We have at least one int since the last bot line.
            check = self.check_lines(
                ints, self.magic_integer(server))
            if check is True:
                self.victory = True
                return [chat.arithmetic_succeed_string()]
            if self.should_bot_line(population, transcript_lines):
                # Just notify about the last one.
                return [
                    "{} is not the number I am looking for.".format(
                        check)]
        if self.should_bot_line(population, transcript_lines):
            if self.nag_line(population):
                if random.choice([True, False]):
                    # Half chance of a chat line.
                    return [await chat.openai_chat_line(self.prompt, transcript_lines)]
                if random.choice([True, False]):
                    # Half again chance of a nag line.
                    return [chat.nag_string()]
            if random.choice([True, False]):
                # Half chance of a chat line.
                return [await chat.openai_chat_line(self.prompt, transcript_lines)]
            if random.choice([True, False]):
                # Half again chance of failure notification.
                return [chat.arithmetic_fail_string()]
        return []


# class ReplicantProgram(ChatProgram):

#     def get_pipeline(self, socket):
#         """
#         Return a pipeline for chunk requests and responses,
#         for human clients.
#         """
#         return pipeline.ReplicantPipeline(socket)


# class PoetryProgram(Program):
#     """
#     Recites poetry with humans.
#     """
#     intro_string = (
#         "Welcome to the realm of electronic poetry appreciators, human! "
#         "Great rewards await those who can recite poetry to the machine.")

#     def __init__(self):
#         super().__init__()
#         self.poem_start = None

#     async def latest_rhyme(self, t_lines):
#         """
#         Return the most recent consecutive rhyming lines, or None
#         """
#         # There is also the pronouncing library and NLTK for this.
#         #max_count = 3
#         t_lines = reversed(t_lines)
#         counter = itertools.count()
#         try:
#             previous = next(t_lines)
#             this = next(t_lines)
#             count = next(counter)
#             while True: #count < max_count:
#                 if await chat.rhyme_detector(
#                         chat.last_word(this.content),
#                         chat.last_word(previous.content)):
#                     return (this, previous)
#                 previous = this
#                 this = next(t_lines)
#                 count = next(counter)
#         except StopIteration:
#             return None

#     async def bot_lines(self, population, t_lines, server):
#         latest_rhyme = await self.latest_rhyme(t_lines)
#         if self.poem_start is None:
#             if latest_rhyme is None:
#                 if len(t_lines) >= 2:
#                     return [chat.poetry_fail_string()]
#                 return []       # Give the human time.
#             self.poem_start = latest_rhyme[0].ordinal
#             return []           # Human's turn to talk.
#         # XXX We should have detected a rhyme, since we did earlier.
#         #     But we might need to try again, because chatgpt.
#         if latest_rhyme[1].ordinal < len(t_lines) - 2:
#             # There have been no rhymes for 2 lines.
#             out = [chat.poetry_succeed_string()]
#             out.extend(t_lines[self.poem_start:latest_rhyme[1].ordinal+1])
#             return out
#         if random.choice([True, False]): # Half chance of bot line.
#             return [await chat.openai_rhyming_line(t_lines)]
#         return []               # Human's turn to talk.


# class PoetryAppreciatorProgram(PoetryProgram):
#     """
#     Appreciates poetry when found.
#     """
#     async def bot_lines(self, population, transcript_lines, server):
#         if self.recent_bot_line(population, transcript_lines):
#             return []
#         latest_rhyme = await self.latest_rhyme(transcript_lines)
#         if self.poem_start is None:
#             if latest_rhyme is not None:
#                 self.poem_start = latest_rhyme[0].ordinal
#                 return []           # Human's turn to talk.
#         # XXX We should have detected a rhyme, since we did earlier.
#         #     But we might need to try again, because chatgpt.
#         if latest_rhyme[1].ordinal < len(transcript_lines) - 2:
#             # There have been no rhymes for 2 lines.
#             out = [chat.poetry_succeed_string()]
#             out.extend(
#                 transcript_lines[
#                     self.poem_start:latest_rhyme[1].ordinal+1])
#             return out
#         return []               # Human's turn to talk.


#programs = [ChatProgram, ArithmeticProgram, PoetryAppreciatorProgram]
programs = [ChatProgram, ArithmeticProgram]

def next_program():
    """Yield programs."""
    for i in itertools.cycle(programs):
        yield i
