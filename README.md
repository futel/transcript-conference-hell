# Transcript Conference Hell

Services used:

- DigitalOcean Networking, App Platform
- Twilio Calls API
- OpenAI API

# Setup

To be done once.

- have futel/transcript-conference-hell repo with dev branch on github
- add app-dev.phu73l.net DigitalOcean domain

The local environment is only used for testing.

- virtualenv -p python3 env
- source env/bin/activate
- pip install -r src/requirements.txt
- pip install python-dotenv

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

# Unit test

- source env/bin/activate
- ./test.py

# Smoke integration test

- source env/bin/activate
- ./itest.py
- ./test_chat.py
- ./test_program.py
- ./test_server.py

# Smoke deployed integration test

Hit the URL on the TwiML page e.g.

    wget https://ws.app-dev.phu73l.net/index.xml

# Notes

https://docs.digitalocean.com/products/app-platform/reference/app-spec/
https://docs.digitalocean.com/tutorials/app-deploy-flask-app/
https://github.com/digitalocean/sample-python/tree/main
https://platform.openai.com/docs/api-reference/chat/create

If we use 100 tokens per gpt-3.5-turbo roundtrip, $0.0002/request.
Estimate 10 requests per minute, $0.002/minute
