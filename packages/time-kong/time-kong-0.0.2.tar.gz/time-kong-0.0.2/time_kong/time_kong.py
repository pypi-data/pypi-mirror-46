#!/usr/bin/env python
# -*- coding: utf8 -*-
# Author: Tony <stayblank@gmail.com>
# Create: 2019/5/26 21:57
import time
from datetime import datetime

__all__ = ["TimeKong"]


class TimeKong(object):
    FORMATTER = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def timestamp2datetime(timestamp, tz=None):
        return datetime.fromtimestamp(timestamp, tz=tz)

    @classmethod
    def timestamp2string(cls, timestamp, formatter=None):
        d = cls.timestamp2datetime(timestamp)
        return cls.datetime2string(d, formatter)

    @staticmethod
    def datetime2timestamp(d):
        a = time.mktime(d.timetuple())
        b = d.microsecond / 1e6
        return a + b

    @classmethod
    def datetime2string(cls, d, formatter=None):
        formatter = formatter or cls.FORMATTER
        return d.strftime(formatter)

    @classmethod
    def string2timestamp(cls, s, formatter=None):
        d = cls.string2datetime(s, formatter)
        return cls.datetime2timestamp(d)

    @classmethod
    def string2datetime(cls, s, formatter=None):
        formatter = formatter or cls.FORMATTER
        return datetime.strptime(s, formatter)

    @classmethod
    def floor_to_millisecond(cls, timestamp):
        return round(timestamp, 3)

    @classmethod
    def floor_to_second(cls, timestamp):
        return round(timestamp, 1)

    @classmethod
    def floor_to_minute(cls, timestamp):
        d = cls.timestamp2datetime(timestamp)
        floor_d = datetime(year=d.year, month=d.month, day=d.day, hour=d.hour, minute=d.minute)
        return cls.datetime2timestamp(floor_d)

    @classmethod
    def floor_to_hour(cls, timestamp):
        d = cls.timestamp2datetime(timestamp)
        floor_d = datetime(year=d.year, month=d.month, day=d.day, hour=d.hour)
        return cls.datetime2timestamp(floor_d)

    @classmethod
    def floor_to_day(cls, timestamp):
        d = cls.timestamp2datetime(timestamp)
        floor_d = datetime(year=d.year, month=d.month, day=d.day)
        return cls.datetime2timestamp(floor_d)

    @classmethod
    def floor_to_month(cls, timestamp):
        d = cls.timestamp2datetime(timestamp)
        floor_d = datetime(year=d.year, month=d.month, day=1)
        return cls.datetime2timestamp(floor_d)

    @classmethod
    def floor_to_year(cls, timestamp):
        d = cls.timestamp2datetime(timestamp)
        floor_d = datetime(year=d.year, month=1, day=1)
        return cls.datetime2timestamp(floor_d)
