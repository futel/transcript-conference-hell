"""
Download all transcripts from the S3 bucket.
"""
# We don't have real packages.
import sys
sys.path.append('src')

import asyncio
import dotenv
import os

dotenv.load_dotenv('.env')

from unittest import mock

import call
#import util

async def test_call():
    to_address = 'sip:demo1@conference-hell-dev.sip.twilio.com'
    #to_address = 'sip:clinton@direct-futel-prod.sip.twilio.com'
    await call.call_random()
    #await call.call(to_address)


asyncio.run(test_call())
