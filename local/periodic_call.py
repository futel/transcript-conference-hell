#!/usr/bin/env python

import dotenv
dotenv.load_dotenv()

import asyncio
import itertools
import os
import random
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

from_number = '+15032126803'
to_addresses_extensions = [
    'sip:demo1@futel-conference.sip.twilio.com',
    'sip:demo2@futel-conference.sip.twilio.com',
    'sip:demo3@futel-conference.sip.twilio.com',
    'sip:demo4@futel-conference.sip.twilio.com',
    'sip:demo5@futel-conference.sip.twilio.com',
    'sip:demo6@futel-conference.sip.twilio.com',
    'sip:demo7@futel-conference.sip.twilio.com',
    'sip:demo8@futel-conference.sip.twilio.com',
    'sip:demo9@futel-conference.sip.twilio.com']

to_addresses_futel = [
    '+15039266271',
    '+15034449412',
    '+15039266341',
    '+17345476651',
    '+13602282259',
    '+15039266188',
    '+13132469283',
    '+15034836584',
    '+15033889637',
    '+15039465227',
    '+15032945966',
    '+15039288465',
    '+15034448615']

min_ring = 6
max_ring = 15

client = Client(account_sid, auth_token)

async def call(to_address):
    ring_secs = random.randint(min_ring, max_ring)
    print(to_address, ring_secs)
    # Call hangs up immediatly on pickup. User's ATA
    # initiates a new call. This probably won't work.
    # twiml='<Response><Hangup/></Response>',
    call = client.calls.create(
        url="https://ws.app-dev.phu73l.net/index.xml",
        #twiml='<Response><Hangup/></Response>',
        method='GET',
        to=to_address,
        from_=from_number)
    print(call)
    await asyncio.sleep(ring_secs)
    # Cancel the call if it has not been answered. This
    # probably hangs up on people because the resource
    # status is not up to date.
    call = client.calls(call.sid).fetch()
    if call.status != 'in-progress':
        call = client.calls(call.sid).update(status='completed')
        print(to_address, 'canceled')
    else:
        print(to_address, call.status)

async def main():
    tasks = []
    # Should simultaneously ring futel phones.
    while True:
        to_address = random.choice(to_addresses_extensions)
        tasks.append(asyncio.create_task(call(to_address)))
        to_address = random.choice(to_addresses_futel)
        tasks.append(asyncio.create_task(call(to_address)))
        to_address = random.choice(to_addresses_futel)
        tasks.append(asyncio.create_task(call(to_address)))
        wait_secs = random.randint(min_ring+2, max_ring+5)
        await asyncio.sleep(wait_secs)

asyncio.run(main())
