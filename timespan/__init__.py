# import api inspired by the asterisk phone system, which lets you
# define timespans in the 'business hours' sense, using strings to
# describe your time intervals, and then check if a datetime falls
# within those intervals.
from timespan.asterisk import match, match_one

# import api inspired by microsoft .net which lets you define time
# deltas using a popular string syntax.
from timespan.dotnet import to_string, from_string, total_seconds, \
  c, constant, g, general_short, G, general_long
