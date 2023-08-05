# coding=utf-8
#
# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Most of this work is copyright (C) 2013-2019 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.
#
# END HEADER

"""
--------------------
hypothesis[dateutil]
--------------------

This module provides ``dateutil`` timezones.

You can use this strategy to make
:py:func:`hypothesis.strategies.datetimes` and
:py:func:`hypothesis.strategies.times` produce timezone-aware values.
"""

from __future__ import absolute_import, division, print_function

import datetime as dt

from dateutil import tz, zoneinfo  # type: ignore

import hypothesis._strategies as st

__all__ = ["timezones"]


def __zone_sort_key(zone):
    """Sort by absolute UTC offset at reference date,
    positive first, with ties broken by name.
    """
    assert zone is not None
    offset = zone.utcoffset(dt.datetime(2000, 1, 1))
    offset = 999 if offset is None else offset
    return (abs(offset), -offset, str(zone))


@st.cacheable
@st.defines_strategy
def timezones():
    # type: () -> st.SearchStrategy[dt.tzinfo]
    """Any timezone in dateutil.

    This strategy minimises to UTC, or the timezone with the smallest offset
    from UTC as of 2000-01-01, and is designed for use with
    :py:func:`~hypothesis.strategies.datetimes`.

    Note that the timezones generated by the strategy may vary depending on the
    configuration of your machine. See the dateutil documentation for more
    information.
    """
    all_timezones = sorted(
        [tz.gettz(t) for t in zoneinfo.get_zonefile_instance().zones],
        key=__zone_sort_key,
    )
    all_timezones.insert(0, tz.UTC)
    # We discard Nones in the list comprehension because Mypy knows that
    # tz.gettz may return None.  However this should never happen for known
    # zone names, so we assert that it's impossible first.
    assert None not in all_timezones
    return st.sampled_from([z for z in all_timezones if z is not None])
