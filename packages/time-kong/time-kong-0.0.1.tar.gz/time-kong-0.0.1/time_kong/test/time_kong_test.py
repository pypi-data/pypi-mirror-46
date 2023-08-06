#!/usr/bin/env python
# -*- coding: utf8 -*-
# Author: Tony <stayblank@gmail.com>
# Create: 2019/5/26 23:02
from datetime import datetime
import unittest

from time_kong import TimeKong


class TestTimeKong(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_datetime2timestamp(self):
        d = datetime(year=2019, month=5, day=26, hour=22, minute=42, second=26, microsecond=330232)
        ts = TimeKong.datetime2timestamp(d)
        self.assertEqual(1558881746.330232, ts)


if __name__ == "__main__":
    unittest.main()
