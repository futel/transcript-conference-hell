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
    num_human_lines = 1         # Human lines before bot talks.

    def __init__(self):
        util.log('Initializing program {}'.format(
            self.__class__.__name__))
        self.prompt = next(prompt_cycle)
        self.victory = False

    def intro_text(self, socket, population):
        return "Welcome to transcription hell, human!"

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
        # Two thirds chance of bot line.
        return random.choice([True, True, False])

    # async def bot_lines(self, population, transcript_lines, server):
    #     """
    #     Return a list of zero or more chat lines.
    #     """
    #     if self.should_bot_line(transcript_lines):
    #         bot_line = await self.bot_line(population, transcript_lines, server)
    #         if bot_line:
    #             return [bot_line]
    #     return []

    def handle_dtmf(self, _message, _socket, _latest_socket, _sockets):
        return []


class ChatProgram(Program):
    """
    Chats with humans.
    """
    async def bot_lines(self, population, transcript_lines, server):
        """Possibly return a list of strings for the bot to say."""
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


class ReplicantProgram(Program):

    def __init__(self):
        super().__init__()
        self.started = False

    def intro_text(self, socket, population):
        out = "Welcome to the replicant challenge! "
        if self.started:
            out += (
                "One human has been replaced with a bot. "
                "Press any key when the bot is speaking to identify it. "
                "Don't falsely accuse a human!")
        else:
            if population <= 3:
                out += "We need at least three humans to start. "
            out += "Press any key when you are ready. "
        return out

    def succeed_string(self):
        strs = [
            "You have succeeded in identifying the bot.",
            "You have identified the bot. Victory!",
            "Victory! You have identified the bot."]
        return random.choice(strs)

    def fail_human_string(self):
        strs = [
            "Someone has falsely accused a human."]
        return random.choice(strs)

    def fail_bot_string(self):
        strs = [
            "Someone accused me. You always knew I was a bot, I don't count."]
        return random.choice(strs)

    def handle_dtmf(self, _message, socket, latest_socket, sockets):
        """
        Handle DTMF message. Check and set victory or possibly return a list of
        strings for the bot to say.
        """
        # XXX The bot human may have quit. We could restart here and kluge in
        #     another bot for next time.
        if not self.started:
            population = len(sockets)
            if population >= 3:
                self.started = True
                # Mark a human as a bot.
                socket = random.choice(list(sockets))
                socket.attrs['bot'] = True
            return [self.intro_text(socket, population)]

        announcements = []
        if latest_socket == None: # latest_socket is the bot facilitator.
            announcements.append(self.fail_bot_string())
        elif latest_socket.attrs.get('bot'):
            # Latest_socket was marked as a bot, the user chose correctly.
            self.victory = True
            if latest_socket == socket:
                # Socket successfully accused itself, special announce
                announcements.append("The bot has correctly accused itself.")
            announcements.append(self.succeed_string())
            # Remove all bot attributes from the humans.
            for socket in sockets:
                socket.attrs['bot'] = False
        else:                   # latest_socket is a human.
            announcements.append(self.fail_human_string())
        return announcements

    async def bot_lines(self, population, transcript_lines, server):
        """
        Check and set victory or possibly return a list of strings for the bot
        to say.
        """
        return []


class ArithmeticProgram(Program):
    num_human_lines = 1

    def fail_string(self):
        strs = [
            "Incorrect!",
            "That is not correct. Try again. I believe in you.",
            "You have failed.",
            "You have failed. Try again. I believe in you.",
            "Your arithmetic skills are inferior.",
        ]
        return random.choice(strs)

    def succeed_string(self):
        strs = [
            "That is correct!",
            "That is correct. Thank you.",
            "You have succeeded.",
            "You have completed the challenge.",
            "You have completed the challenge. Thank you for your service.",
            "Your arithmetic skills are superior.",
            "Your arithmetic skills are superior. Thank you for your service.",
        ]
        return random.choice(strs)

    def intro_text(self, socket, population):
        intro_string = (
            "Welcome to the arithmetic challenge! "
            "Each human has an integer. "
            "To succeed, state the sum of all the integers.")
        out = "Your integer is {}.".format(
            self.sid_to_integer(socket.stream_sid))
        return intro_string + out

    def word_to_integer(self, w):
        """Return the integer corresponding to w, or None."""
        if w.isdigit():
            return int(w)
        # This might not be necessary in practice, and we get false positives.
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
        """
        Check and set victory or possibly return a list of strings for the bot
        to say.
        """
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
                return [self.succeed_string()]
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
                return [self.fail_string()]
        return []


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

# def poetry_fail_string():
#     """Return a poetry fail string."""
#     strs = [
#         "That is not a poem. I want a poem.",
#         "You can do better than that. Tell me a poem.",
#         "Tell me a poem. Try again.",
#         "I demand a poem.",
#         "I want a poem.",
#         "I want a poem. Give me a poem.",
#         "I want a poem. Try again.",
#         "Please give me a poem. Try again."]
#     return random.choice(strs)

# def poetry_succeed_string():
#     """Return a poetry succeed string."""
#     strs = [
#         "That is a poem. Thank you.",
#         "Thank you for the poem.",
#         "Thank you for the poem. I like it.",
#         "Thank you for the poem. I like you.",
#         "That is a poem!",
#         "Poem collection successful!",
#         "Poem status: affirmitve."]
#     return random.choice(strs)

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


programs = [ReplicantProgram, ChatProgram, ArithmeticProgram]

def next_program():
    """Yield programs."""
    for i in itertools.cycle(programs):
        yield i
