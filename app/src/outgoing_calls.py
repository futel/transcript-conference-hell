#!/usr/bin/env python
"""
Call an extension and connect it to the conference.
"""


import asyncio
import base64
import json
import random
import time
from twilio.rest import Client

import chat
import pipeline
import program
import lines
import speech
import util

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']


async def call(to_address):
    ring_secs = random.randint(min_ring, max_ring)
    call = client.calls.create(
        url="https://ws.app-dev.phu73l.net/index.xml",
        method='GET',
        to=to_address,
        from_=from_number)
    await asyncio.sleep(ring_secs)
    # Cancel the call if it has not been answered. This
    # probably hangs up on people because the resource
    # status is not up to date. The correct way is to have
    # a webook cancel a task when the call is answered.
    call = client.calls(call.sid).fetch()
    if call.status != 'in-progress':
        call = client.calls(call.sid).update(status='completed')
        util.log('outgoing_calls', to_address, call.status, 'canceled')
    else:
        util.log('outgoing_calls', to_address, call.status)
