# SIP client setup

# Requirements

## Set up SIP client on Twilio

SIP client should be set up as listed in twilio.md.

# Set up Polycom SoundPoint IP 501

See client.md on twilio-sip-server.

XXX primary-sip-server conference-hell-dev.sip.twilio.com

# Set up Grandstream HT701 etc

See client.md on twilio-sip-server.

XXX primary-sip-server conference-hell-dev.sip.twilio.com

# Test

XXX update

# Setup

XXX update

Register SIP client to sip:experimenter@futel-experimenter.sip.twilio.com.

Have Twilio test PSTN number <FROM_PSTN_NUMBER>

## Call SIP client

XXX update

    twilio api:core:calls:create --from="<FROM_PSTN_NUMBER>" --to="sip:experimenter@futel-experimenter.sip.twilio.com" --url="https://ws.app-dev.phu73l.net/index.xml" --method=GET

## Call PSTN number

XXX update

    twilio api:core:calls:create --from="<FROM_PSTN_NUMBER>" --to="<PSTN_NUMBER>" --url="https://ws.app-dev.phu73l.net/index.xml" --method=GET
