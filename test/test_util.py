import unittest
from unittest import mock

import util


class TestUtil(unittest.TestCase):

    @mock.patch.object(
        util, 'boto3', new_callable=mock.Mock)
    def test_write_lines_s3(self, mock_boto3):
        util.write_lines_s3()
