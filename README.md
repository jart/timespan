# timespan

Utilities for working with popular timespan formats.

## .Net Timespans

Functions are provided for converting between .NET 7.0 TimeSpan objects
(with format specifiers) and Python's `datetime.timedelta` objects.

### `timespan.from_string(str) -> timedelta`

Converts a TimeSpan string in the current locale to a
`datetime.timedelta` object, e.g.

    >>> import timespan
    >>> timespan.c(3, 17, 25, 30, 500)
    '3.17:25:30.5000000'
    >>> timespan.from_string('3.17:25:30.5000000')
    datetime.timedelta(days=3, seconds=62730, microseconds=500000)

#### Parameters

- `timespan_string`: TimeSpan string of any format and locale.

#### Return Value

A timedelta object.

### `timespan.to_string(specifier: str, *args: tuple) -> str`

Converts date\time information (variable-length tuple) to a TimeSpan
string in the current locale.

#### Parameters

- `specifier`: format specifier. Options are 'c', 'g' and 'G'.
- `args`: variable-length tuple (size 1, 3, 4 or 5) specifying
  components of date and time.

#### Return Value

A TimeSpan string

### Notes

See the switch case of `_args_to_seconds()` in
[src/timespan/dotnet.py](src/timespan/dotnet.py) for full coverage of
all input types.

## Asterisk Timespans

Asterisk style timespans allow you to check if a timestamp falls within
a specified list of boundaries. For example, you might want to program
your phone system to only accept calls Mon-Fri from 9 a.m. to 5 p.m.
except on holidays like Christmas.

Timespans are specified in the form of `times|daysofweek|days|months`.
If your timespan starts with `!`, it'll only match if the timestamps
falls outside the given range.

Basic example:

    import timespan
    from datetime import datetime

    business_hours = [
        '9:00-17:00|mon-fri|*|*',  # is between 9 a.m. to 5 p.m. on Mon to Fri
        '!*|*|1|jan',              # not new years
        '!*|*|25|dec',             # not christmas
        '!*|thu|22-28|nov',        # not thanksgiving
    ]

    if timespan.match(business_hours, datetime.now()):
        print "we're open for business!"
    else:
        print "sorry, we're closed :("

For more examples, see the documentation or source code.
