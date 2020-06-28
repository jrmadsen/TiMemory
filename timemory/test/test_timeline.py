#!@PYTHON_EXECUTABLE@
# MIT License
#
# Copyright (c) 2018, The Regents of the University of California,
# through Lawrence Berkeley National Laboratory (subject to receipt of any
# required approvals from the U.S. Dept. of Energy).  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from __future__ import absolute_import

__author__ = "Muhammad Haseeb"
__copyright__ = "Copyright 2020, The Regents of the University of California"
__credits__ = ["Muhammad Haseeb"]
__license__ = "MIT"
__version__ = "@PROJECT_VERSION@"
__maintainer__ = "Jonathan Madsen"
__email__ = "jrmadsen@lbl.gov"
__status__ = "Development"

import os
import time
import json
import random
import unittest
import threading
import inspect
import numpy as np
import timemory as tim
from timemory import component as comp
from timemory.profiler import profile
from timemory.bundle import auto_timer, auto_tuple, marker

# --------------------------- test setup variables ----------------------------------- #


# --------------------------- helper functions ----------------------------------------- #

# check availability of a component
def check_available(component):
    return inspect.isclass(component)


# compute fibonacci
def fibonacci(n):
    return n if n < 2 else (fibonacci(n-1) + fibonacci(n-2))


def fib(n, instr):
    if instr == True:
        with marker(components=["wall_clock"], key="fib"):
            return n if n < 2 else (fib(n - 1, True) + fib(n - 2, False))

    else:
        return n if n < 2 else (fibonacci(n-1) + fibonacci(n-2))


# sleep for n millisec
def do_sleep(n):
    time.sleep(n * 1e-3)


# cpu utilization for n millisec
def consume(n):
    # Python 3.7 has time_ns()
    try:
        # get current time in nsec
        now = time.time_ns()
        # try until time point
        while(time.time_ns() < (now + (n * 1e6))):
            pass
    except:
        now = 1000 * time.time()
        # try until time point
        while((1000 * time.time()) < (now + n)):
            pass


# get a random entry
def random_entry(vect):
    random.seed(int(1.0e9 * time.time()))
    num = int(random.uniform(0, len(vect) - 1))
    return vect[num]


# get auto_tuple config
def get_config(items=["wall_clock"]):
    return [getattr(tim.component, x) for x in items]


# -------------------------- Thottle Tests set ---------------------------------------- #
# Timeline tests class
class TimemoryTimelineTests(unittest.TestCase):
    # setup class: timemory settings
    @classmethod
    def setUpClass(self):
        # set up environment variables
        os.environ["TIMEMORY_TIMELINE_PROFILE"] = "ON"
        tim.settings.verbose = 1
        tim.settings.debug = False
        tim.settings.json_output = True
        tim.settings.mpi_thread = False
        tim.settings.dart_output = True
        tim.settings.dart_count = 1
        tim.settings.banner = False

        tim.settings.parse()

        # put one empty marker
        with marker(components=["wall_clock"], key=''):
            pass

    def setUp(self):
        # set up environment variables
        os.environ["TIMEMORY_TIMELINE_PROFILE"] = "ON"
        tim.settings.parse()

    # Tear down class: timemory_finalize
    @classmethod
    def tearDownClass(self):
        # timemory finalize
        # tim.timemory_finalize()
        # tim.dmp.finalize()
        pass

    # ---------------------------------------------------------------------------------- #
    # test profiler_depth
    def test_parse(self):
        """
        parse
        """
        tim.settings.timeline_profile = False
        os.environ["TIMEMORY_TIMELINE_PROFILE"] = "ON"
        tim.settings.parse()

        print("timeline_profile() = ", tim.settings.timeline_profile)
        ret = os.environ.get("TIMEMORY_TIMELINE_PROFILE")

        print("environment = ", ret)
        self.assertTrue(ret)
        self.assertTrue(tim.settings.timeline_profile)

    # ---------------------------------------------------------------------------------- #
    # test profiler_depth
    def test_no_timeline(self):
        """
        no timeline
        """
        old_data = tim.get()["timemory"]["ranks"][0]["value0"]["graph"]
        os.environ["TIMEMORY_TIMELINE_PROFILE"] = "OFF"

        tim.settings.parse()
        n = 5
        with marker(components=["wall_clock"], key=self.shortDescription()):
            with profile(components=["wall_clock"]):
                ret = fibonacci(n)
                print("\nfibonacci({}) = {}".format(n, ret))

        # counts must be == 1
        data = tim.get()["timemory"]["ranks"][0]["value0"]["graph"]
        #print("\n{}".format(json.dumps(data, indent=4, sort_keys=True)))
        maxcnt = 1
        for k in data:
            if k not in old_data:
                self.assertTrue(k["stats"]["count"] >= 1)
                maxcnt = max(k["stats"]["count"], maxcnt)
        self.assertTrue(maxcnt > 1)

    # ---------------------------------------------------------------------------------- #
    # test profiler_depth
    def test_timeline(self):
        """
        timeline
        """
        n = 5

        old_data = tim.get()["timemory"]["ranks"][0]["value0"]["graph"]

        with marker(components=["wall_clock"], key=self.shortDescription()):
            with profile(components=["wall_clock"]):
                ret = fibonacci(n)
                print("\nfibonacci({}) = {}".format(n, ret))

        # inspect data
        data = tim.get()["timemory"]["ranks"][0]["value0"]["graph"]
        #print("\n{}".format(json.dumps(data, indent=4, sort_keys=True)))

        # counts must be == 1
        for k in data:
            if k not in old_data:
                self.assertTrue(k["stats"]["count"] == 1)


# ----------------------------- main test runner ---------------------------------------- #
# main runner
def run():
    # run all tests
    unittest.main()


if __name__ == '__main__':
    run()
