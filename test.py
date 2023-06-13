#!/usr/bin/env python3

import dotenv
import unittest

dotenv.load_dotenv()
loader = unittest.TestLoader()
tests = loader.discover('test')
testRunner = unittest.runner.TextTestRunner()
testRunner.run(tests)
