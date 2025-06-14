import asyncio
import os
import random
from twilio.rest import Client

import util

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

from_number = '+15032126803'
to_addresses_extensions = [
    'sip:demo1@conference-hell-dev.sip.twilio.com',
    'sip:demo2@conference-hell-dev.sip.twilio.com',
    'sip:demo3@conference-hell-dev.sip.twilio.com',
    'sip:demo4@conference-hell-dev.sip.twilio.com',
    'sip:demo5@conference-hell-dev.sip.twilio.com',
    'sip:demo6@conference-hell-dev.sip.twilio.com']

to_addresses_futel_extensions = [
    "sip:ainsworth@direct-futel-prod.sip.twilio.com",
    "sip:alleytwentyseventh@direct-futel-prod.sip.twilio.com",
    "sip:brazee@direct-futel-prod.sip.twilio.com",
    "sip:breckenridge@direct-futel-prod.sip.twilio.com",
    "sip:central@direct-futel-prod.sip.twilio.com",
    "sip:cesar-chavez-one@direct-futel-prod.sip.twilio.com",
    "sip:clinton@direct-futel-prod.sip.twilio.com",
    "sip:eighth@direct-futel-prod.sip.twilio.com",
    "sip:fortysecond@direct-futel-prod.sip.twilio.com",
    "sip:killingsworth@direct-futel-prod.sip.twilio.com",
    "sip:landline@direct-futel-prod.sip.twilio.com",
    "sip:microcosm@direct-futel-prod.sip.twilio.com",
    "sip:saratoga@direct-futel-prod.sip.twilio.com",
    "sip:souwester@direct-futel-prod.sip.twilio.com",
    "sip:street-roots-one@direct-futel-prod.sip.twilio.com",
    "sip:taylor@direct-futel-prod.sip.twilio.com",
    "sip:upright@direct-futel-prod.sip.twilio.com"]

# to_addresses_futel = [
#     '+15039266271',
#     '+15034449412',
#     '+15039266341',
#     '+17345476651',
#     '+13602282259',
#     '+15039266188',
#     '+13132469283',
#     '+15034836584',
#     '+15033889637',
#     '+15039465227',
#     '+15032945966',
#     '+15039288465',
#     '+15034448615']

client = Client(account_sid, auth_token)

async def call(to_address, timeout):
    # URL to render twiml for callee to experience.
    # Top URL which the sip domains send callers to.
    url = "https://ws.conference-hell-dev.phu73l.net/index.xml",
    call = client.calls.create(
        url=url,
        method='GET',
        timeout=timeout,
        to=to_address,
        from_=from_number)
    util.log(call.status)

async def call_random():
    """Call random destinations and connect to the conference hell."""
    for i in range(2):
        # Ring timeout in seconds, about 5s/ring.
        timeout = random.randint(1, 19)
        to_address = random.choice(to_addresses_extensions)
        asyncio.create_task(call(to_address, timeout))
        await asyncio.sleep(1)
    for i in range(10):
        # Ring timeout in seconds, about 5s/ring.
        timeout = random.randint(15, 29)
        to_address = random.choice(to_addresses_futel_extensions)
        asyncio.create_task(call(to_address, timeout))
