# Unit test

- source venv/bin/activate
- pytest test

# Smoke integration test

- source venv/bin/activate
- itest/itest.py
- itest/test_chat.py
- itest/test_pipeline.py
- itest/test_program.py
- itest/test_server.py

# Smoke deployed integration test

Hit the URL on the TwiML page e.g.

    wget https://ws.conference-hell-dev.phu73l.net/index.xml

# Manual test

Register SIP client demo1 to conference-hell-dev.sip.twilio.com, interact.

# View logs

Get the app ID.

- doctl --config conf/config.yaml apps list

View logs

- doctl apps logs <id> -f
