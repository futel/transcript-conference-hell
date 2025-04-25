#!/usr/bin/env python3

import dotenv
import os

dotenv.load_dotenv()
with open('app.yaml.template', 'r') as f:
    template = f.read()
    print(
        template.format(
            AWS_ACCESS_KEY_ID=os.environ['AWS_ACCESS_KEY_ID'],
            AWS_SECRET_ACCESS_KEY=os.environ['AWS_SECRET_ACCESS_KEY'],
            GOOGLE_CREDS_JSON=os.environ['GOOGLE_CREDS_JSON'],
            OPENAI_API_KEY=os.environ['OPENAI_API_KEY']))
