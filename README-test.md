# Unit test

- source env/bin/activate
- ./test.py

# Smoke integration test

- source env/bin/activate
- ./itest.py
- ./test_chat.py
- ./test_pipeline.py
- ./test_program.py
- ./test_server.py

# Smoke deployed integration test

Hit the URL on the TwiML page e.g.

    wget https://ws.app-dev.phu73l.net/index.xml
