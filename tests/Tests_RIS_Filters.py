#MIT License

#Copyright (c) 2026 Richard S. Graham

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


import os
import os.path
import sys
import unittest

sys.path.append(os.path.expanduser("../") )
import RIS_to_jobs as RIS


class TestStatusFilter(unittest.TestCase):
    def test_exclude(self):
        expected_none = ["Bid Unsuccessful - failed!",
                         "Withdrawen - Bid Unsuccessful"]
        for status in expected_none:
            self.assertEqual(RIS.status_filter(status), "Exclude")

    def test_success(self):
        expected_success = ["Project Live",
                         ]
        for status in expected_success:
            self.assertEqual(RIS.status_filter(status), "Funding Awarded")

    def test_pre_submission(self):
        expected_pre_submission = ["Bid Development",
                         ]
        for status in expected_pre_submission:
            self.assertEqual(RIS.status_filter(status), "Pre-submission")

    def test_submitted(self):
        expected_submitted = ["Bid Awaiting Response",
                         ]
        for status in expected_submitted:
            self.assertEqual(RIS.status_filter(status), "Submitted to Funder")


    def test_unspecified(self):
        expected_none = ["Bid Unsuccess",
                         "Unsuccessful"]
        for status in expected_none:
            self.assertEqual(RIS.status_filter(status), "Unspecified")


class TestJobFamilyFilter(unittest.TestCase):
    def test_RandT(self):
        expected_RT = ["R&T Research 4 AUG2018 RT4-R / 30",
                        "R&T who cares whats next", "Casual R&T Teaching 4" ]

        for grade in expected_RT:
            self.assertEqual(RIS.job_family_filter(grade,""), "Research & Teaching")

    def test_APM(self):
        expected_APM = ["APM Research 4 AUG2018 RT4-R / 30",
                        "APM who cares whats next","APM 5 CES (0.5FTE)" ]

        for grade in expected_APM:
            self.assertEqual(RIS.job_family_filter(grade,""), "Administrative, Professional & Managerial")

    def test_Technical_Services(self):
        expected_TS = ["Technical Services 4 AUG2018 RT4-R / 30",
                        "Technical Services who cares whats next","Technical Services 5 CES (0.5FTE)" ]

        for grade in expected_TS:
            self.assertEqual(RIS.job_family_filter(grade,"Technician (later text does not matter)"), "Technical Services")
            self.assertEqual(RIS.job_family_filter(grade,"text does not matter"), "Technical Services")


unittest.main(argv=["first-arg-is-ignored"], exit=False)



