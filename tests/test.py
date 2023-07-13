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

import doctest
import math
import tqdm
import timespan

MAX_TEST_VAL = 1000000  # maximal value to test. its additive inverse number is the minimal value to test
TEST_STEP = 0.987654321  # difference between consecutive test values. should be a number slightly less than 1.0
TEST_PRECISION = 1e-6  # sufferable absolute difference of the required result when converting


def _test(start, stop, step):
    """
    Iterative test of converting float values to TimeSpan and back to float, verifying the value is kept
    """

    num_vals = int((stop - start) / step)
    stop = start + (num_vals + 1) * step
    test_values = (start + i * step for i in range(num_vals))

    print(
        f"Testing {num_vals} values in range",
        f"{timespan.g(start)} : {timespan.g(stop)}",
        f"with specifiers {{c,g,G}}",
    )
    for test_time in tqdm.tqdm(test_values, total=num_vals):
        for timespan_ctor in (timespan.c, timespan.g, timespan.G):
            string_from_float = timespan_ctor(test_time)
            float_from_string = timespan.from_string(string_from_float).total_seconds()
            assert math.isclose(test_time, float_from_string, abs_tol=TEST_PRECISION),\
                (test_time, float_from_string, timespan_ctor.func.__name__)
    print("Test passed!")


if __name__ == "__main__":
    doctest.testmod(timespan, verbose=True)
    _test(start=-MAX_TEST_VAL, stop=MAX_TEST_VAL, step=TEST_STEP)  # guarantees at least 2*MAX_TEST_VAL values were tested
