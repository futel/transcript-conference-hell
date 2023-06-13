"""Client to output chat transcriptions."""

import asyncio
import openai

import lines
import util


chat_label = "Franz"

prompt = """
Complete this dialog by completing the last line of dialog, spoken by "{}". Add only one line.

Dialog:
{}
{}:
"""

# system_message = (
#     "You are writing a script. The characters are trying to understand how to cooperate to share vital information. They are confused and wondering who is hostile, who is friendly, and who has a clue. Statements are short.. Complete the next statement as if Franz said it.")

def generate_prompt(lines):
    return prompt.format(chat_label, '\n'.join(lines), chat_label)

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

async def chat_line(lines):
    response = await openai.Completion.acreate(
       model="text-davinci-003",
       prompt=generate_prompt(lines),
       temperature=0.6)
    response = response.choices[0].text
    # # ChatCompletion lets us use better models than Completion.
    # # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb
    # response = await openai.ChatCompletion.acreate(
    #     # "gpt-4" "gpt-3.5-turbo" "text-davinci-003"
    #     model="gpt-3.5-turbo",
    #     messages=generate_messages(lines),
    #     temperature=0.8)
    # response = response.choices[0]['message']['content']
    # response = normalize_chat_line(response)
    return response

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
    async def receive_response(self):
        """Generator for responses."""
        while True:
            yield await self.recv_queue.get()
            util.log(f"chatbot sent response")
