# Transcript Conference Hell

Services used:

- DigitalOcean Networking, App Platform
- Twilio Programmable Voice
- Twilio Calls API
- OpenAI API
- Google transcription API

- SIP clients interact with Twilio Programmable Voice components.
- Twilio Programmable Voice components connect to a websocket server running on Digital Ocean App Platform.
- Websocket server interfaces with OpenAI and Google Trascription components.

# Setup

To be done once.

- have futel/transcript-conference-hell repo with dev branch on github
- add app-dev.phu73l.net DigitalOcean domain

Have:

- config.yaml based on config.yaml.sample
- .env based on .env.sample.

Set up the app:

- Install DigitalOcean GitHub app using the web GUI at https://github.com/apps/digitalocean/
  - give it permissions for the futel/transcript-conference-hell repo
  - continue to create the an app with the futel/transcript-conference-hell dev branch, autodeploy
  - edit plan to Basic 1 container, $5/mo
  - region San Francisco
  
App setup creates an app with an unexpected name? We probably didn't nee dto do all of those creation steps above. Anyway, remove it.

# Set up dev instance

Create the app, note the id.

    ./make_app_yaml.py | doctl --config config.yaml apps create --spec -
    
Get the hostname from the "Default Ingress" field of the app. This may take a while before it is available.

    doctl --config config.yaml apps list <id>

Add CNAME for ws.app-dev.phu73l.net pointing to the app's hostname in DigitalOcean domain. Wait for the domain status to be resolved in the app settings page (or just wait longer than the TTL) and for the resulting deploy to finish.

# Deploy dev instance

## Update source

If source has changed, push to transcript-conference-hell dev branch on github.

## Update config

If .do/app.yaml has changed, update config.

Get the app ID.

    doctl --config config.yaml apps list

Update config.

    ./make_app_yaml.py | doctl --config config.yaml apps update <id> --spec -

# Delete dev instance

Get the app ID.

    doctl --config config.yaml apps list

Delete the app.

    doctl --config config.yaml apps delete <id>

---

# Set Up Outgoing Twilio

## Create the Twilio SIP Domain

    twilio api:core:sip:domains:create \
        --domain-name futel-conference.sip.twilio.com \
        --friendly-name futel-conference \
        --sip-registration \
        --voice-method GET \
        --voice-url 'https://ws.app-dev.phu73l.net/index.xml'

## Create the Twilio Credential List

    twilio api:core:sip:credential-lists:create --friendly-name conference

## List the Credential Lists to get the created SID

If we created a new Credential List in the last step, the SID was listed there. Otherwise:

    twilio api:core:sip:credential-lists:list

## Create auth registrations Credential List Mappings

    twilio api:core:sip:domains:auth:registrations:credential-list-mappings:create \
        --domain-sid <DOMAIN SID> \
        --credential-list-sid <CREDENTIAL LIST SID>

## Set voice authentication credentials for SIP Domains

Visit the GUI for the SIP Domain and add the same "conference" credential list to "voice authentication", then save.

There doesn't seem to be any other way to do this.

---

# Set Up Incoming Twilio

## Create Twilio Application Resources (TwiML apps)

    twilio api:core:applications:create \
        --voice-method GET \
        --voice-url 'https://ws.app-dev.phu73l.net/index.xml' \
        --friendly-name "incoming-conference"

## Create a phone number

Use the web GUI; the APIs may allow us to do this, but maybe not.

Create new phone number
- friendly name: conference
- emergency calling: (not registered)
- voice configuration:
    - configure with: TwiML App
    - TwiML App: incoming-conference
- messaging configuation:
    - a message comes in: webhook
    - URL: blank

---

# Add configuration for a new SIP client

## Create credential

List the Credential Lists to get the SID of "conference".

    twilio api:core:sip:credential-lists:list

Create a new credential in the Credential List. Use the SID found in the previous step.

    twilio api:core:sip:credential-lists:credentials:create --credential-list-sid <SID> --username '<USERNAME>' --password '<PASSWORD>'

# Notes

https://docs.digitalocean.com/products/app-platform/reference/app-spec/
https://docs.digitalocean.com/tutorials/app-deploy-flask-app/
https://github.com/digitalocean/sample-python/tree/main

https://platform.openai.com/docs/api-reference/chat/create
https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb


openai billing:
If we use 100 tokens per gpt-3.5-turbo roundtrip, $0.0002/request.
Estimate 10 requests per minute, $0.002/minute
google text to speech billing:
60 mins/mo free

How to store assets? DO Spaces is $5/mo minimum. Twilio service?
