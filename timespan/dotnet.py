# Copyright (c) Microsoft Corporation.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE

import datetime
import locale
import os
import re
from functools import partial

__author__ = "Mattan Serry"
__email__ = "maserry@microsoft.com"
__version__ = "0.1.2"

"""

Module to convert between .NET 7.0 TimeSpan objects (with format specifiers) and Python's datetime.timedelta objects.

References:
https://learn.microsoft.com/en-us/dotnet/api/system.timespan?view=net-7.0
https://learn.microsoft.com/en-us/dotnet/api/system.timespan.-ctor?view=net-7.0
https://learn.microsoft.com/en-us/dotnet/api/system.timespan.tickspersecond?view=net-7.0
https://learn.microsoft.com/en-us/dotnet/standard/base-types/standard-timespan-format-strings?view=new-6.10


The Constant ("c") Format Specifier:
This specifier is not culture-sensitive.
It produces the string representation of a TimeSpan value that is invariant
and that's common to versions prior to .NET Framework 4.
It takes the form [-][d'.']hh':'mm':'ss['.'fffffff]
For example:



>>> c(0, 0, 30, 0)
'00:30:00'
>>> from_string('00:30:00')
datetime.timedelta(seconds=1800)

>>> c(3, 17, 25, 30, 500)
'3.17:25:30.5000000'
>>> from_string('3.17:25:30.5000000')
datetime.timedelta(days=3, seconds=62730, microseconds=500000)



The General Short ("g") Format Specifier:
This specifier outputs only what is needed.
It is locale-sensitive and takes the form [-][d':']h':'mm':'ss[.FFFFFFF]
For example:

>>> g(1, 3, 16, 50, 500)
'1:3:16:50.5'
>>> from_string('1:3:16:50.5')
datetime.timedelta(days=1, seconds=11810, microseconds=500000)

>>> g(1, 3, 16, 50, 599)
'1:3:16:50.599'
>>> from_string('1:3:16:50.599')
datetime.timedelta(days=1, seconds=11810, microseconds=599000)



The General Long ("G") Format Specifier:
This specifier always outputs days and seven fractional digits.
It is locale-sensitive and takes the form [-]d':'hh':'mm':'ss.fffffff
For example:

>>> G(18, 30, 0)
'0:18:30:00.0000000'
>>> from_string('0:18:30:00.0000000')
datetime.timedelta(seconds=66600)

Running this file will invoke doctest, which will verify that the above running examples hold true.
It will also invoke a test that checks the conversions for about 2 million different values.
Microsecond-level precision is guaranteed.

"""

_TICKS_PER_SECOND = 1e7
_PATTERN = re.compile(
    r'^'
    r'(?P<sign>-?)'
    r'(?P<days>\d+[:.])?'
    r'(?P<hours>\d{1,2}):'
    r'(?P<minutes>\d{2}):'
    r'(?P<seconds>\d{2})'
    r'(?P<fraction>[.,]\d{1,7})?'
    r'$'
)
_FORMAT_SPECIFIERS = ('c', 'g', 'G')
# Different locales use different decimal point characters. For example, en-US locale uses '.' and fr-FR locale uses ','
_NUMBER_DECIMAL_SEPARATOR = os.environ.get("TIMESPAN_LOCALE", locale.localeconv()["decimal_point"])


def _args_to_seconds(args, *, by_ticks=False) -> float:
    """
    Converts a time information tuple to total seconds as float, passing through a timedelta object.
    @param args: variable-length tuple (size 1, 3, 4 or 5) specifying components of date and time.
    See the switch case of this function for full coverage of all input types.
    @param by_ticks: specifies input as ticks instead of seconds.
    @return: total seconds float.

    For example:
    >>> _args_to_seconds([100])
    100.0
    >>> _args_to_seconds([100], by_ticks=True)
    1e-05
    >>> _args_to_seconds([1, 2])
    Traceback (most recent call last):
    ...
    ValueError: Cannot initialize a TimeSpan instance with 2 arguments

    """

    days, hours, minutes, seconds, milliseconds = 0, 0, 0, 0, 0

    if len(args) == 1:
        arg, = args
        if by_ticks:
            arg = arg / _TICKS_PER_SECOND
        seconds = arg

    elif len(args) == 3:
        # Initializes a new instance to a specified number of hours, minutes, and seconds.
        hours, minutes, seconds = args

    elif len(args) == 4:
        # Initializes a new instance to a specified number of days, hours, minutes, and seconds.
        days, hours, minutes, seconds = args

    elif len(args) == 5:
        # Initializes a new instance to a specified number of days, hours, minutes, seconds, and milliseconds.
        days, hours, minutes, seconds, milliseconds = args
    else:
        raise ValueError(f"Cannot initialize a TimeSpan instance with {len(args)} arguments")

    return datetime.timedelta(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        milliseconds=milliseconds,
    ).total_seconds()


def to_string(specifier: str, *args: tuple) -> str:
    """
    Converts date\time information (variable-length tuple) to a TimeSpan string in the current locale.
    @param specifier: format specifier. Options are 'c', 'g' and 'G'.
    @param args: variable-length tuple (size 1, 3, 4 or 5) specifying components of date and time.
    See the switch case of _args_to_seconds for full coverage of all input types.
    @return: TimeSpan string.
    See examples at module-level docs.
    """
    assert specifier in _FORMAT_SPECIFIERS

    # convert the date\time information tuple to total seconds as float
    seconds: float = _args_to_seconds(args)

    # break seconds to components
    delta = datetime.timedelta(seconds=abs(seconds))
    d = delta.days
    h, remainder = divmod(delta.seconds, 3600)
    m, s = divmod(remainder, 60)
    f = delta.microseconds * 10

    # apply format-specific style for hours, minutes and seconds
    h = str(h).zfill(1 if specifier == 'g' else 2)
    m = str(m).zfill(2)
    s = str(s).zfill(2)

    # apply format-specific style for fraction
    if f > 0 or specifier == 'G':
        f = ('.' if specifier == 'c' else _NUMBER_DECIMAL_SEPARATOR) + str(f).rjust(7, '0')
        if specifier == 'g':
            f = f.rstrip('0')
    else:
        f = ''

    # apply format-specific style for days
    if d > 0 or specifier == 'G':
        d = str(d) + ('.' if specifier == 'c' else ':')
    else:
        d = ''

    # build and return final string
    sign = '-' if seconds < 0 else ''
    return f"{sign}{d}{h}:{m}:{s}{f}"


def from_string(timespan_string: str) -> datetime.timedelta:
    """
    Converts a TimeSpan string in the current locale to a datetime.timedelta object.
    Analogous to TimeSpan.Parse - https://learn.microsoft.com/en-us/dotnet/api/system.timespan.parse?view=net-7.0
    @param timespan_string: TimeSpan string of any format and locale.
    @return: A timedelta object.
    See examples at module-level docs.
    """

    groups = _PATTERN.match(timespan_string).groupdict()
    sign = -1 if groups['sign'] == '-' else 1
    days = sign * int((groups['days'] or '0').rstrip(':.'))
    hours = sign * int(groups['hours'])
    minutes = sign * int(groups['minutes'])
    seconds = sign * int(groups['seconds'])
    fraction = sign * float(groups['fraction'] or 0.0)
    delta = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds + fraction)
    return delta


def total_seconds(timespan_string: str) -> float:
    """
    Converts a TimeSpan string in the current locale to a datetime.timedelta object.
    Analogous to TimeSpan.Parse with TimeSpan.TotalSeconds.
    See more:
    https://learn.microsoft.com/en-us/dotnet/api/system.timespan.parse?view=net-7.0
    https://learn.microsoft.com/en-us/dotnet/api/system.timespan.totalseconds?view=net-7.0
    @param timespan_string: TimeSpan string of any format and locale.
    @return: Total seconds as float.
    """
    delta = from_string(timespan_string)
    seconds = delta.total_seconds()
    return seconds


constant = partial(to_string, 'c')
general_short = partial(to_string, 'g')
general_long = partial(to_string, 'G')

c = constant
g = general_short
G = general_long
