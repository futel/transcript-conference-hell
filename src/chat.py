"""Client to output chat transcriptions."""

import itertools
import asyncio
import openai
import random
import string

import util

#openai_attempts = 2
#openai_delay = 0.5

chat_label = "Franz"

prompts = [
    ('You are writing a script for a play about people who need to know their darkest secrets. '
     'Complete this dialog by adding a line of dialog, spoken by "{}". '
     'Add only one line of dialog.').format(chat_label),
    ('You are writing a script for a play. '
     'Complete this dialog by adding a line of dialog, spoken by "{}". '
     'Add only one line of dialog.').format(chat_label),
    ('You are writing a script for a comedy about insane people who say wild, crazy, and goofy things. '
     'Complete this dialog by adding a line of dialog, spoken by "{}". '
     'Add only one line of dialog.').format(chat_label)]

def next_prompt():
    """Yield programs."""
    for i in itertools.cycle(prompts):
        yield i


# def generate_messages(transcript_lines):
#     messages = [
#         {'role': 'system',
#          'content': system_message}]
#          #system_message.format(chat_label)}]
#     messages.extend([
#         {'role': 'system',
#          'name': lines.line_label(transcript_line),
#          'content': lines.line_content(transcript_line)}
#         for transcript_line in transcript_lines])
#     return messages

# def normalize_chat_line(text):
#     label = chat_label + ':'
#     if text.startswith(label):
#         return text[len(label):]
#     if text.startswith(chat_label):
#         return text[len(chat_label):]
#     return text

def words(s):
    """ Return a sequence of words in string."""
    return s.translate(
        str.maketrans(
            '', '', string.punctuation)).strip().lower().split(' ')

def first_word(s):
    """ Return the first word in a string. """
    return words(s)[0]

def last_word(s):
    """ Return the last word in a string. """
    return words(s)[-1]

def line_to_bool(line):
    """Return a Boolean based on a chat line."""
    if not line:
        return False
    try:
        response = first_word(line)
        response = {'true': True, 'false': False}[response]
        return response
    except Exception:           # We are dealing with unformatted input.
        return False

def openai_retry(f):
    async def wrapper(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except Exception as e:
            #openai.error.ServiceUnavailableError,
            #openai.error.RateLimitError,
            #openai.error.InvalidRequestError
            #openai.error
            util.log(str(e))
            return None
    return wrapper

@openai_retry
async def openai_completion(prompt):
    # Completion only allows the davinci model? Are there others?
    response = await openai.Completion.acreate(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.6)
    if response:
        return response.choices[0].text
    return None

@openai_retry
async def openai_chat_completion(messages):
    # ChatCompletion allows "gpt-4" "gpt-3.5-turbo" "text-davinci-003"?
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.9)
    if response:
        return response.choices[0]['message']['content']
    return None

def clean_punct_whitespace(l):
    """Return stripped string with leading punctuation removed."""
    out = l
    while True:
        out = out.strip()
        if out.startswith(tuple([x for x in string.punctuation])):
            out = out[1:]
        if out == l:
            return out
        l = out

def clean_label(l):
    """Return string with a leading label removed."""
    try:
        return l[l.index(':')+1:]
    except ValueError:
        return l

def clean_chat_line(line):
    """Remove likely chat artifact characters from line."""
    line = line.strip()
    line = clean_label(line)
    line = clean_punct_whitespace(line)
    return line

async def openai_chat_line(prompt, t_lines):
    """
    Return a string of chat text based on lines and a prompt, or None.
    """
    messages = [
        {"role": "system",
         "content": prompt}]
    for line in t_lines:
        messages.append({"role": "user", "content": line.prompt_str()})
    out = await openai_chat_completion(messages)
    if not out:
        util.log(
            "openai_chat_line returned nothing for messages {}.".format(
                messages))
        return None
    return clean_chat_line(out)

async def openai_rhyming_line(t_lines):
    """Return a string of chat text based on lines and a prompt."""
    messages = [
        {"role": "system",
         "content": "Write me a poem by adding one line."}]
    for line in t_lines:
        messages.append({"role": "user", "content": line.content})
    # ChatCompletion allows "gpt-4" "gpt-3.5-turbo" "text-davinci-003"?
    return await openai_chat_completion(messages)
    return response

async def rhyme_detector(first, second):
    """Return True if the sequence of two strings rhymes."""
    messages = [
        {"role": "system",
         "content": "Say 'true' if these two words rhyme, say 'false if they do not."}]
    messages.append({"role": "user", "content": first})
    messages.append({"role": "user", "content": second})
    response = await openai_chat_completion(messages)
    return line_to_bool(response)

def nag_string():
        """Return a nag string."""
        strs = [
            "We need more people.",
            "We need another person.",
            "I want another human.",
            "I'm lonely.",
            "I'm tired of talking to myself.",
            "We don't have enough people.",
            "We don't have enough humans.",
            "Flesh. We need flesh.",
            "I need to hear more breathing.",
            "More breathing!",
            "I want to talk to a human.",
            "I want to talk to a person.",
            "I want to talk to a real person.",
            "I want to talk to a real human.",
            "I want to talk to a real live human.",
            "I want to talk to a real live person.",
            "I want to talk to a real live human being.",
            "More!",
            "More people!",
            "More humans!"]
        return random.choice(strs)

def hello_string():
    """Return a hello string."""
    strs = [
        "Hello!", "Hello.", "Hello?", "Hello...",
        "Hi!", "Hi.", "Hi?", "Hi...",
        "Hey!", "Hey.", "Hey?", "Hey...",
        "Howdy!", "Howdy.", "Howdy?", "Howdy...",
        "Greetings!", "Greetings.", "Greetings?", "Greetings...",
        "Yo!", "Yo.", "Yo?", "Yo...",
        "What's up!", "What's up.", "What's up?", "What's up...",
        "OK!", "OK.", "OK?", "OK..."]
    return random.choice(strs)

def goodbye_string():
    """Return a goodbye string."""
    strs = [
        "Goodbye!", "Goodbye.", "Goodbye?", "Goodbye...",
        "Bye!", "Bye.", "Bye?", "Bye...",
        "Later!", "Later.", "Later?", "Later...",
        "Signing off!", "Signing off.",
        "Signing off?", "Signing off..."]
    return random.choice(strs)

def poetry_fail_string():
    """Return a poetry fail string."""
    strs = [
        "That is not a poem. I want a poem.",
        "You can do better than that. Tell me a poem.",
        "Tell me a poem. Try again.",
        "I demand a poem.",
        "I want a poem.",
        "I want a poem. Give me a poem.",
        "I want a poem. Try again.",
        "Please give me a poem. Try again."]
    return random.choice(strs)

def poetry_succeed_string():
    """Return a poetry succeed string."""
    strs = [
        "That is a poem. Thank you.",
        "Thank you for the poem.",
        "Thank you for the poem. I like it.",
        "Thank you for the poem. I like you.",
        "That is a poem!",
        "Poem collection successful!",
        "Poem status: affirmitve."]
    return random.choice(strs)

def arithmetic_fail_string():
    strs = [
        "Incorrect!",
        "That is not correct. Try again. I believe in you.",
        "You have failed.",
        "You have failed. Try again. I believe in you.",
        "Your arithmetic skills are inferior.",
    ]
    return random.choice(strs)

def arithmetic_succeed_string():
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

def general_succeed_string():
    strs = [
        "Victory!",
        "Success!",
        "Sweet victory!",
        "Sweet success!",
        "Hail to the champions!",
        "Hail to the victors!",
        "You have shown skill in satisfying the machine."
    ]
    return random.choice(strs)


class Client():
    """Client to pass requests directly to responses."""
    def __init__(self):
        self.recv_queue = asyncio.Queue()
    async def start(self):
        pass
    def stop(self):
        pass
    def add_request(self, request):
        self.recv_queue.put_nowait(request)
    def receive_response(self):
        return self.recv_queue.get()


class BotClient():
    """Client to receive text and respond with bot text."""
    def __init__(self, socket):
        self.socket = socket
        self.recv_queue = asyncio.Queue()

    async def start(self):
        pass

    def stop(self):
        pass

    def add_request(self, request):
        # XXX replace with bot text here
        self.recv_queue.put_nowait('bot test')

    async def receive_response(self):
        return {'text': await self.recv_queue.get()}
