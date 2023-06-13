# Requirements

- Have Credential List 'experimenter' with credential 'experimenter'
- Have SIP Domain 'futel-experimenter' with SIP registartion enabled, voice authentication and SIP registration for 'experimenter' Credential List
- Have a Twilio phone number

# Test

# Setup

Register SIP client to sip:experimenter@futel-experimenter.sip.twilio.com.

Have Twilio test PSTN number <FROM_PSTN_NUMBER>

## Call SIP client

    twilio api:core:calls:create --from="<FROM_PSTN_NUMBER>" --to="sip:experimenter@futel-experimenter.sip.twilio.com" --url="https://ws.app-dev.phu73l.net/index.xml" --method=GET

## Call PSTN number

    twilio api:core:calls:create --from="<FROM_PSTN_NUMBER>" --to="<PSTN_NUMBER>" --url="https://ws.app-dev.phu73l.net/index.xml" --method=GET
