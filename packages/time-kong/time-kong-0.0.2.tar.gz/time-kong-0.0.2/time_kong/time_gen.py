#!/usr/bin/env python
# -*- coding: utf8 -*-
# Author: Tony <stayblank@gmail.com>
# Create: 2019/5/26 22:19
__all__ = ["TimeGen"]


class TimeGen(object):
    ONE_MILLISECOND = 0.001
    ONE_SECOND = 1
    ONE_MINUTE_SECONDS = 60 * ONE_SECOND
    ONE_HOUR_SECONDS = 60 * ONE_MINUTE_SECONDS
    ONE_DAY_SECONDS = 24 * ONE_HOUR_SECONDS
    ONE_MONTH_SECONDS = 30 * ONE_DAY_SECONDS
    ONE_YEAR_SECONDS = 365 * ONE_MONTH_SECONDS

    @classmethod
    def n_milliseconds(cls, n):
        return n * cls.ONE_MILLISECOND

    @classmethod
    def n_seconds(cls, n):
        return n * cls.ONE_SECOND

    @classmethod
    def n_minutes(cls, n):
        return n * cls.ONE_MINUTE_SECONDS

    @classmethod
    def n_hours(cls, n):
        return n * cls.ONE_HOUR_SECONDS

    @classmethod
    def n_days(cls, n):
        return n * cls.ONE_DAY_SECONDS

    @classmethod
    def n_months(cls, n):
        return n * cls.ONE_MONTH_SECONDS

    @classmethod
    def n_years(cls, n):
        return n * cls.ONE_YEAR_SECONDS
