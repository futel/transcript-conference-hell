# Setup

- virtualenv -p python3 env
- source env/bin/activate
- pip install -r src/requirements.txt
- pip install python-dotenv

# Unit test

- source env/bin/activate
- test/test.py

# Smoke integration test

- source env/bin/activate
- itest/itest.py
- itest/test_chat.py
- itest/test_pipeline.py
- itest/test_program.py
- itest/test_server.py

# Smoke deployed integration test

Hit the URL on the TwiML page e.g.

    wget https://ws.app-dev.phu73l.net/index.xml
