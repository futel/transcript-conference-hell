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

# Meta-requirements

Domains should be created with DigitalOcean:
- conference-hell-dev.phu73l.net

Repo should be on GitHub

- futel/transcript-conference-hell

DigitalOcean GitHub app should be installed
- https://github.com/apps/digitalocean/
- add permissions for futel/transcript-conference-hell repository

Twilio should be set up as described in twilio.md.

XXX AWS? Metrics/logging?

# Requirements

- debian box (trixie, ubuntu 23)
- Python 3.11-3.12, but this should be Python 3.10
- doctl
  - sudo snap install doctl

# Setup

To be done once.

## Create deployment virtualenv

- python3 -m venv venv
- source venv/bin/activate
- pip install -r src/requirements.txt
- pip install python-dotenv pytest

## Set up doctl

- https://docs.digitalocean.com/products/app-platform/how-to/create-apps
- create access token
  - name transcript-conference-hell
  - no expire
  - scopes full access XXX?
  - save in conf
- grant acccess with token, and use
  - doctl auth init --context transcript-conference-hell
  - doctl auth switch --context transcript-conference-hell

## Populate config

- config.yaml based on config.yaml.sample.
- .env based on .env.sample.

# Set up dev instance

App setup creates an app with an unexpected name? We probably didn't need to do all of those creation steps above. Anyway, remove it.

Create the app, note the id.

- source venv/bin/activate
- ./make_app_yaml.py | doctl --config conf/config.yaml apps create --spec -
    
Get the hostname from the "Default Ingress" field of the app. This may take a while before it is available.

Add CNAME for ws.conference-hell-dev.phu73l.net pointing to the app's hostname in DigitalOcean domain. Wait for the domain status to be resolved in the app settings page (or just wait longer than the TTL) and for the resulting deploy to finish.

# Deploy dev instance

## Update source

If source has changed, push to dev branch of transcript-conference-hell repo.

## Update config

Get the app ID.

- doctl --config conf/config.yaml apps list

Update config.

- source venv/bin/activate
- ./make_app_yaml.py | doctl --config conf/config.yaml apps update <id> --spec -

# Delete dev instance

Get the app ID.

- doctl --config conf/config.yaml apps list

Delete the app.

- doctl --config conf/config.yaml apps delete <id>
