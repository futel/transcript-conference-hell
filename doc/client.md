# SIP client setup

# Requirements

## Set up SIP client on Twilio

SIP client should be set up as listed in twilio.md.

# Set up Polycom SoundPoint IP 501

See client.md on twilio-sip-server.

# Set up Grandstream HT701

See client.md on twilio-sip-server.

# Test

XXX update

# Setup

Register SIP client to sip:experimenter@futel-experimenter.sip.twilio.com.

Have Twilio test PSTN number <FROM_PSTN_NUMBER>

## Call SIP client

    twilio api:core:calls:create --from="<FROM_PSTN_NUMBER>" --to="sip:experimenter@futel-experimenter.sip.twilio.com" --url="https://ws.app-dev.phu73l.net/index.xml" --method=GET

## Call PSTN number

    twilio api:core:calls:create --from="<FROM_PSTN_NUMBER>" --to="<PSTN_NUMBER>" --url="https://ws.app-dev.phu73l.net/index.xml" --method=GET
