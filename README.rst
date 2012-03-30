.. -*-rst-*-

==========
 timespan
==========

:name:        timespan
:description: Check if timestamp falls within specific boundaries
:copyright:   © 2012 Justine Alexandra Roberts Tunney
:license:     MIT


What Is This?
=============

Timespans allow you to check if a timestamp falls within a specified list of
boundaries.  For example, you might want to program your phone system to only
accept calls Mon-Fri from 9 a.m. to 5 p.m. except on holidays like Christmas.

Timespans are specified in the form of ``times|daysofweek|days|months``.  If
your timespan starts with ``!``, it'll only match if the timestamps falls
outside the given range.

Basic example::

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


Installation
============

From folder::

    sudo python setup.py install

From cheeseshop::

    sudo pip install timespan

From git::

    sudo pip install git+git://github.com/jart/timespan.git
