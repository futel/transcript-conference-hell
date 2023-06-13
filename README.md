# Setup

Services used:

- DigitalOcean Networking, App Platform
- Twilio Calls API
- OpenAI API

To be done once.

- have apps-experimenter repo with dev branch on github
- add app-dev.phu73l.net DigitalOcean domain

- virtualenv -p python3 env
- source env/bin/activate
- pip install -r requirements.txt
- pip install python-dotenv

Have:

- config.yaml based on config.yaml.sample
- .env based on .env.sample.

# Set up dev instance

Create the app, note the id.

    ./make_app_yaml.py | doctl --config config.yaml apps create --spec -
    
Get the hostname from the "Default Ingress" field of the app. This may take a while before it is available.

    doctl --config config.yaml apps list <id>

Add CNAME for ws.app-dev.phu73l.net pointing to the app's hostname in DigitalOcean domain. Wait for the domain status to be resolved in the settings page (or just wait longer than the TTL) and for the resulting deploy to finish.

# Deploy dev instance

## Update source

If source has changed, push to apps-experimenter dev branch on github.

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
- ./test_server.py

# Smoke deployed integration test

Hit the URL on the TwiML page e.g.

    wget https://ws.app-dev.phu73l.net/index.xml

# Notes

https://docs.digitalocean.com/products/app-platform/reference/app-spec/
https://docs.digitalocean.com/tutorials/app-deploy-flask-app/
https://github.com/digitalocean/sample-python/tree/main
