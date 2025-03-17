# Unit test

- source env/bin/activate
- pytest test

# Smoke integration test

- source env/bin/activate
- itest/itest.py
- itest/test_chat.py
- itest/test_pipeline.py
- itest/test_program.py
- itest/test_server.py

# Smoke deployed integration test

Hit the URL on the TwiML page e.g.

    wget https://ws.conference-hell-dev.phu73l.net/index.xml
