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

import datetime
import os
import os.path
import sys

sys.path.append(os.path.expanduser("../") )

import unittest

import RIS_to_jobs as RIS


class TestBasicReader(unittest.TestCase):
    def test_initial_basic(self):
        filename = "Example_Exports/Project57324957EPSRCexample.xlsx"

        myExtractor = RIS.JobExtractor(filename)
        myJobs = myExtractor.get_jobs_list()
        self.assertEqual(len(myJobs), 2)

        self.assertEqual(myJobs[0].label, "Monte Carlo Post-doc")
        self.assertEqual(myJobs[0].role_type, "Fellow")
        self.assertEqual(myJobs[0].grade, "R&T Research 4 AUG2025 RT4-R / 31")
        self.assertEqual(myJobs[0].start_date, datetime.datetime(2026, 9, 1, 0, 0))
        self.assertEqual(myJobs[0].length_in_months, 36)
        self.assertEqual(myJobs[0].fte_percent, 100)

        self.assertEqual(myJobs[1].label, "Quantum Chemistry Post-Doc")
        self.assertEqual(myJobs[1].role_type, "Fellow")
        self.assertEqual(myJobs[1].grade, "R&T Research 4 AUG2025 RT4-R / 28")
        self.assertEqual(myJobs[1].start_date, datetime.datetime(2026, 9, 1, 0, 0))
        self.assertEqual(myJobs[1].length_in_months, 36)
        self.assertEqual(myJobs[1].fte_percent, 100)


    def test_second_basic(self):
        filename = "Example_Exports/SecondExample.xlsx"

        myExtractor = RIS.JobExtractor(filename)
        myJobs = myExtractor.get_jobs_list()
        self.assertEqual(len(myJobs), 2)

        self.assertEqual(myJobs[0].label, "Experimentalist")
        self.assertEqual(myJobs[0].role_type, "Fellow")
        self.assertEqual(myJobs[0].grade, "R&T Research 4 AUG2025 RT4-R / 31")
        self.assertEqual(myJobs[0].start_date, datetime.datetime(2027, 11, 19, 0, 0))
        self.assertEqual(myJobs[0].length_in_months, 17)
        self.assertEqual(myJobs[0].fte_percent, 50)

        self.assertEqual(myJobs[1].label, "Theoretical Chemist")
        self.assertEqual(myJobs[1].role_type, "Fellow")
        self.assertEqual(myJobs[1].grade, "R&T Research 4 AUG2025 RT4-R / 28")
        self.assertEqual(myJobs[1].start_date, datetime.datetime(2029, 2, 23, 0, 0))
        self.assertEqual(myJobs[1].length_in_months, 24)
        self.assertEqual(myJobs[1].fte_percent, 80)

    def test_longer_grant(self):
        filename = "Example_Exports/Project5931919410yearsofresearch.xlsx"

        myExtractor = RIS.JobExtractor(filename)
        myJobs = myExtractor.get_jobs_list()
        self.assertEqual(len(myJobs), 4)

        self.assertEqual(myJobs[0].label, "Simulation post-doc")
        self.assertEqual(myJobs[0].role_type, "Fellow")
        self.assertEqual(myJobs[0].grade, "R&T Research 4 AUG2025 RT4-R / 30")
        self.assertEqual(myJobs[0].start_date, datetime.datetime(2026, 11, 17, 0, 0))
        self.assertEqual(myJobs[0].length_in_months, 54)
        self.assertEqual(myJobs[0].fte_percent, 100)

        self.assertEqual(myJobs[1].label, "Theory post-doc")
        self.assertEqual(myJobs[1].role_type, "Fellow")
        self.assertEqual(myJobs[1].grade, "R&T Research 4A AUG2025 RT4A-R / 30")
        self.assertEqual(myJobs[1].start_date, datetime.datetime(2026, 9, 1, 0, 0))
        self.assertEqual(myJobs[1].length_in_months, 60)
        self.assertEqual(myJobs[1].fte_percent, 33)

        self.assertEqual(myJobs[2].label, "Senior project manager")
        self.assertEqual(myJobs[2].role_type, "Professional enabling staff (Incurs Overheads)")
        self.assertEqual(myJobs[2].grade, "APM5 AUG2025 APM5 / 40")
        self.assertEqual(myJobs[2].start_date, datetime.datetime(2028, 6, 13, 0, 0))
        self.assertEqual(myJobs[2].length_in_months, 21)
        self.assertEqual(myJobs[2].fte_percent, 100)

        self.assertEqual(myJobs[3].label, "Lab Technician")
        self.assertEqual(myJobs[3].role_type, "Technician (Incurs Overheads)")
        self.assertEqual(myJobs[3].grade, "Technician 4 AUG2025 TS4 / 27")
        self.assertEqual(myJobs[3].start_date, datetime.datetime(2026, 9, 1, 0, 0))
        self.assertEqual(myJobs[3].length_in_months, 60)
        self.assertEqual(myJobs[3].fte_percent, 100)




unittest.main(argv=["first-arg-is-ignored"], exit=False)



