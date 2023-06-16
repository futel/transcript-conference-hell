"""Client to output chat transcriptions."""

import asyncio
import openai
import random
import string

import lines
import util


chat_label = "Franz"

chat_prompt = """
Complete this dialog by completing the last line of dialog, spoken by "{}". Add only one line.

Dialog:
{}
{}:
"""

def format_chat_prompt(t_lines):
    return chat_prompt.format(chat_label, '\n'.join(t_lines), chat_label)

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

# async def chat_line(lines):
#     """Return a string of chat text based on lines and a prompt."""
#     # ChatCompletion lets us use better models than Completion.
#     # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb
#     response = await openai.ChatCompletion.acreate(
#         # "gpt-4" "gpt-3.5-turbo" "text-davinci-003"
#         model="gpt-3.5-turbo",
#         messages=generate_messages(lines),
#         temperature=0.8)
#     response = response.choices[0]['message']['content']
#     return response

def line_to_bool(line):
    """Return a Boolean based on a chat line."""
    try:
        response = line.translate(
            str.maketrans(
                '', '', string.punctuation)).strip().lower().split(' ')[0]
        response = {'true': True, 'false': False}[response]
        return response
    except Exception:           # We are dealing with unformatted input.
        return False

async def chat_line(t_lines):
    """Return a string of chat text based on lines and a prompt."""
    # Completion only allows the davinci model? Are there others?
    response = await openai.Completion.acreate(
        model="text-davinci-003",
        prompt=format_chat_prompt(t_lines),
        temperature=0.6)
    response = response.choices[0].text
    return response

async def rhyming_line(t_lines):
    """Return a string of chat text based on lines and a prompt."""
    t_lines = lines.line_contents(t_lines)
    messages = [
        {"role": "system",
         "content": "Write me a poem by adding one line."}]
    for line in t_lines:
        messages.append({"role": "user", "content": line})
    # ChatCompletion allows "gpt-4" "gpt-3.5-turbo" "text-davinci-003"?
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.6)
    response = response.choices[0]['message']['content']
    return response

async def rhyme_detector(t_lines):
    """Return True if content of the last two t_lines rhyme."""
    try:
        t_lines = reversed([t_lines.pop(), t_lines.pop()])
    except IndexError:
        return False
    t_lines = lines.line_contents(t_lines)
    messages = [
        {"role": "system",
         "content": "Say 'true' if these two lines rhyme, say 'false if they do not."}]
    for line in t_lines:
        messages.append({"role": "user", "content": line})
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.6)
    response = response.choices[0]['message']['content']
    response = line_to_bool(response)
    return response

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


class Client():
    """Client to pass requests directly to responses."""
    def __init__(self):
        self.recv_queue = asyncio.Queue()
    async def start(self):
        util.log("chatbot client starting")
    def stop(self):
        util.log("chatbot client stopped")
    def add_request(self, text):
        self.recv_queue.put_nowait(text)
    def receive_response(self):
        return self.recv_queue.get()
