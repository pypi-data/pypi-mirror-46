# TimeKong

![time kong](https://github.com/PurpleSun/time_kong/blob/master/time-kong-logo.png?raw=true "time kong")

Time converter between timestamp, string and datetime.


## Installation

You can install `time-kong` simply with `pip`:

```
pip install time-kong
```


## Usages

### TimeKong
```python
from datetime import datetime

from time_kong import TimeKong

ts = 1558883766.864879
TimeKong.timestamp2string(ts, formatter="%Y-%m-%d %H:%M:%S.%f")
# '2019-05-26 23:16:06.864879'
TimeKong.timestamp2datetime(ts)
# datetime.datetime(2019, 5, 26, 23, 16, 6, 864879)

ds = '2019-05-26 23:16:06.864879'
TimeKong.string2timestamp(ds, formatter="%Y-%m-%d %H:%M:%S.%f")
# 1558883766.864879
TimeKong.string2datetime(ds, formatter="%Y-%m-%d %H:%M:%S.%f")
# datetime.datetime(2019, 5, 26, 23, 16, 6, 864879)

dt = datetime(year=2019, month=5, day=26, hour=22, minute=42, second=26, microsecond=864879)
TimeKong.datetime2timestamp(dt)
# 1558881746.864879
TimeKong.datetime2string(dt, formatter="%Y-%m-%d %H:%M:%S.%f")
# '2019-05-26 22:42:26.864879'
```

### TimeGen
```python
from time_kong import TimeGen

# generate time in second quickly
print "42 milliseconds is %s second" % TimeGen.n_milliseconds(42)
print "42 seconds is %s seconds" % TimeGen.n_seconds(42)
print "42 minutes is %s seconds" % TimeGen.n_minutes(42)
print "42 hours is %s seconds" % TimeGen.n_hours(42)
print "42 days is %s seconds" % TimeGen.n_days(42)
print "42 months is %s seconds" % TimeGen.n_months(42)
print "42 years is %s seconds" % TimeGen.n_years(42)

# 42 milliseconds is 0.042 second
# 42 seconds is 42 seconds
# 42 minutes is 2520 seconds
# 42 hours is 151200 seconds
# 42 days is 3628800 seconds
# 42 months is 108864000 seconds
# 42 years is 39735360000 seconds
```

Constants

1. `TimeGen.ONE_MILLISECOND`
2. `TimeGen.ONE_SECOND`
3. `TimeGen.ONE_MINUTE_SECONDS`
4. `TimeGen.ONE_HOUR_SECONDS`
5. `TimeGen.ONE_DAY_SECONDS`
6. `TimeGen.ONE_MONTH_SECONDS`
7. `TimeGen.ONE_YEAR_SECONDS`


## Author

time-kong is developed and maintained by fanwei.zeng (stayblank@gmail.com). It can be found here:

https://github.com/PurpleSun/time_kong