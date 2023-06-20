# Set up Grandstream HT701

basic settings
telnet server: no

advanced settings
admin password:
firmware server path: blank
config server path: blank
automatic upgrade: no
always skip the firmware check: selected

fxs port
account active: yes
primary sip server: futel-conference.sip.twilio.com
nat traversal: no
sip user id: <extension>
authenticate id: <extension>
authenticate password: <password>
sip registration: yes
unregister on reboot: no
outgoing call without registration: yes
Disable Call-Waiting: yes
Disable Call-Waiting Caller ID: yes
Disable Call-Waiting Tone: yes
Use # As Dial Key: no
Offhook Auto-Dial: 1
Offhook Auto-Dial Delay: 0
Hook Flash Timing: minimum: 500 maximum: 500
 

# Test

# Setup

Register SIP client to sip:experimenter@futel-experimenter.sip.twilio.com.

Have Twilio test PSTN number <FROM_PSTN_NUMBER>

## Call SIP client

    twilio api:core:calls:create --from="<FROM_PSTN_NUMBER>" --to="sip:experimenter@futel-experimenter.sip.twilio.com" --url="https://ws.app-dev.phu73l.net/index.xml" --method=GET

## Call PSTN number

    twilio api:core:calls:create --from="<FROM_PSTN_NUMBER>" --to="<PSTN_NUMBER>" --url="https://ws.app-dev.phu73l.net/index.xml" --method=GET
