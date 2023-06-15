import asyncio

import dotenv
dotenv.load_dotenv()

import util
util.cred_kluge()

import speech

async def main():
    client = speech.Client()
    await client.start()
    client.add_request("hello world")
    client.add_request("goodbye world")
    with open("foo", "ab") as f:
        while True:
            response = await client.receive_response()
            print("response")
            f.write(response)

asyncio.run(main())
