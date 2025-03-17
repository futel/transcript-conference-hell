# Twilio deployment

# Requirements

- Twilio CLI package eg twilio-5.22.3-amd64.deb.
- Twilio profile or other way to use creds
  - twilio profiles:create
  - twilio profiles:use [id]

# Setup

To be done once.

## Create the Twilio SIP Domain

    twilio api:core:sip:domains:create \
        --domain-name conference-hell-dev.sip.twilio.com \
        --friendly-name conference-hell-dev \
        --sip-registration \
        --no-emergency-calling-enabled \
        --voice-method GET \
        --voice-url 'https://ws.conference-hell-dev.phu73l.net/index.xml'

## Create the Twilio Credential List

- twilio api:core:sip:credential-lists:create --friendly-name conference-hell

## List the Credential Lists to get the created SID

If we created a new Credential List in the last step, the SID was listed there. Otherwise:

- twilio api:core:sip:credential-lists:list

## Create auth registrations Credential List Mappings

    twilio api:core:sip:domains:auth:registrations:credential-list-mappings:create \
        --domain-sid <SIP DOMAIN SID> \
        --credential-list-sid <CREDENTIAL LIST SID>

## Set voice authentication credentials for SIP Domains

Visit the GUI for the SIP Domain and add the same "conference" credential list to "voice authentication", then save.

There doesn't seem to be any other way to do this.

---

# Set Up Incoming Twilio

## Create Twilio Application Resources (TwiML apps)

    twilio api:core:applications:create \
        --voice-method GET \
        --voice-url 'https://ws.conference-hell-dev.phu73l.net/index.xml' \
        --friendly-name "conference-hell-dev"

## Create a phone number

Use the web GUI; the APIs may allow us to do this, but maybe not.

Create new phone number
- friendly name: conference-hell-dev
- emergency calling: (not registered)
- voice configuration:
    - configure with: TwiML App
    - TwiML App: conference-hell-dev
- messaging configuation:
    - a message comes in: webhook
    - URL: blank

---

# Add configuration for a new SIP client

## Create credential

Create a new credential in the Credential List. Use the SID found in the previous step, or list to get it.

- twilio api:core:sip:credential-lists:list
- twilio api:core:sip:credential-lists:credentials:create --credential-list-sid <SID> --username '<USER>' --password '<PASSWORD>'

# Delete configuration for a SIP client

Delete the credential from the Credential List with the web GUI.
