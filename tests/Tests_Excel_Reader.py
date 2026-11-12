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
import shutil
import sys

sys.path.append(os.path.expanduser("../") )

import unittest

import RIS_to_jobs as RIS


class TestBasicReader(unittest.TestCase):
    def test_initial_basic(self):
        filename = "Project57324957EPSRCexample.xlsx"
        shutil.copyfile(f"Example_Exports/{filename}", f"./{filename}")

        myReader = RIS.ExcelReader(filename)
        myProject = myReader.get_data_object()
        self.assertEqual(myProject.title, "EPSRC example")
        self.assertEqual(myProject.RIS_ID, 57324957)
        self.assertEqual(myProject.PI_name, "Richard Graham")
        self.assertEqual(myProject.PI_username, "pmzrsg")
        self.assertEqual(myProject.lead_unit, "Mathematical Sciences Dept")
        self.assertEqual(myProject.status, "Bid Development")


        self.assertEqual(len(myProject.roles), 2)
        self.assertEqual(myProject.roles[0].label, "Monte Carlo Post-doc")
        self.assertEqual(myProject.roles[0].role_type, "Fellow")
        self.assertEqual(myProject.roles[0].grade, "R&T Research 4 AUG2025 RT4-R / 31")
        self.assertEqual(myProject.roles[0].start_date, datetime.datetime(2026, 9, 1, 0, 0))
        self.assertEqual(myProject.roles[0].length_in_months, 36)
        self.assertEqual(myProject.roles[0].fte_percent, 100)

        self.assertEqual(myProject.roles[1].label, "Quantum Chemistry Post-Doc")
        self.assertEqual(myProject.roles[1].role_type, "Fellow")
        self.assertEqual(myProject.roles[1].grade, "R&T Research 4 AUG2025 RT4-R / 28")
        self.assertEqual(myProject.roles[1].start_date, datetime.datetime(2026, 9, 1, 0, 0))
        self.assertEqual(myProject.roles[1].length_in_months, 36)
        self.assertEqual(myProject.roles[1].fte_percent, 100)

        self.assertEqual(myProject.named_roles, 0)


    def test_second_basic(self):
        filename = "SecondExample.xlsx"
        shutil.copyfile(f"Example_Exports/{filename}", f"./{filename}")

        myReader = RIS.ExcelReader(filename)
        myProject = myReader.get_data_object()

        self.assertEqual(myProject.title, "Different project")
        self.assertEqual(myProject.RIS_ID, 1)
        self.assertEqual(myProject.PI_name, "Bob O'Brian")
        self.assertEqual(myProject.PI_username, "pczbo1")
        self.assertEqual(myProject.lead_unit, "Chemistry Dept")
        self.assertEqual(myProject.status, "Bid Development")

        self.assertEqual(len(myProject.roles), 2)

        self.assertEqual(myProject.roles[0].label, "Experimentalist")
        self.assertEqual(myProject.roles[0].role_type, "Fellow")
        self.assertEqual(myProject.roles[0].grade, "R&T Research 4 AUG2025 RT4-R / 31")
        self.assertEqual(myProject.roles[0].start_date, datetime.datetime(2027, 11, 19, 0, 0))
        self.assertEqual(myProject.roles[0].length_in_months, 17)
        self.assertEqual(myProject.roles[0].fte_percent, 50)

        self.assertEqual(myProject.roles[1].label, "Theoretical Chemist")
        self.assertEqual(myProject.roles[1].role_type, "Fellow")
        self.assertEqual(myProject.roles[1].grade, "R&T Research 4 AUG2025 RT4-R / 28")
        self.assertEqual(myProject.roles[1].start_date, datetime.datetime(2029, 2, 23, 0, 0))
        self.assertEqual(myProject.roles[1].length_in_months, 24)
        self.assertEqual(myProject.roles[1].fte_percent, 80)

    def test_basic_with_named(self):
        filename = "ProjectBasicWithNamed.xlsx"
        shutil.copyfile(f"Example_Exports/{filename}", f"./{filename}")

        myReader = RIS.ExcelReader(filename, verbose=False)
        myProject = myReader.get_data_object()
        self.assertEqual(myProject.title, "EPSRC example")
        self.assertEqual(myProject.RIS_ID, 57324957)
        self.assertEqual(myProject.PI_name, "Richard Graham")
        self.assertEqual(myProject.PI_username, "pmzrsg")
        self.assertEqual(myProject.lead_unit, "Mathematical Sciences Dept")
        self.assertEqual(myProject.status, "Bid Development")


        self.assertEqual(len(myProject.roles), 1)
        self.assertEqual(myProject.roles[0].label, "Monte Carlo Post-doc")
        self.assertEqual(myProject.roles[0].role_type, "Fellow")
        self.assertEqual(myProject.roles[0].grade, "R&T Research 4 AUG2025 RT4-R / 31")
        self.assertEqual(myProject.roles[0].start_date, datetime.datetime(2026, 9, 1, 0, 0))
        self.assertEqual(myProject.roles[0].length_in_months, 36)
        self.assertEqual(myProject.roles[0].fte_percent, 100)

        self.assertEqual(myProject.named_roles, 2)


class Test5YearProjectReader(unittest.TestCase):
    def test_read_in(self):
        filename = "Project5931919410yearsofresearch.xlsx"
        shutil.copyfile(f"Example_Exports/{filename}", f"./{filename}")

        myReader = RIS.ExcelReader(filename)
        myProject = myReader.get_data_object()
        self.assertEqual(myProject.title, "10 years of research")
        self.assertEqual(myProject.RIS_ID, 59319194)
        self.assertEqual(myProject.PI_name, "Fiona Frost")
        self.assertEqual(myProject.PI_username, "lizff")
        self.assertEqual(myProject.lead_unit, "HR Business Partnering Policy and Projects")
        self.assertEqual(myProject.status, "Bid Development")

        self.assertEqual(len(myProject.roles), 4)

        self.assertEqual(myProject.roles[0].label, "Simulation post-doc")
        self.assertEqual(myProject.roles[0].role_type, "Fellow")
        self.assertEqual(myProject.roles[0].grade, "R&T Research 4 AUG2025 RT4-R / 30")
        self.assertEqual(myProject.roles[0].start_date, datetime.datetime(2026, 11, 17, 0, 0))
        self.assertEqual(myProject.roles[0].length_in_months, 54)
        self.assertEqual(myProject.roles[0].fte_percent, 100)

        self.assertEqual(myProject.roles[1].label, "Theory post-doc")
        self.assertEqual(myProject.roles[1].role_type, "Fellow")
        self.assertEqual(myProject.roles[1].grade, "R&T Research 4A AUG2025 RT4A-R / 30")
        self.assertEqual(myProject.roles[1].start_date, datetime.datetime(2026, 9, 1, 0, 0))
        self.assertEqual(myProject.roles[1].length_in_months, 60)
        self.assertEqual(myProject.roles[1].fte_percent, 33)
        self.assertEqual(myProject.roles[2].label, "Senior project manager")
        self.assertEqual(myProject.roles[2].role_type, "Professional enabling staff (Incurs Overheads)")
        self.assertEqual(myProject.roles[2].grade, "APM5 AUG2025 APM5 / 40")
        self.assertEqual(myProject.roles[2].start_date, datetime.datetime(2028, 6, 13, 0, 0))
        self.assertEqual(myProject.roles[2].length_in_months, 21)
        self.assertEqual(myProject.roles[2].fte_percent, 100)

        self.assertEqual(myProject.roles[3].label, "Lab Technician")
        self.assertEqual(myProject.roles[3].role_type, "Technician (Incurs Overheads)")
        self.assertEqual(myProject.roles[3].grade, "Technician 4 AUG2025 TS4 / 27")
        self.assertEqual(myProject.roles[3].start_date, datetime.datetime(2026, 9, 1, 0, 0))
        self.assertEqual(myProject.roles[3].length_in_months, 60)
        self.assertEqual(myProject.roles[3].fte_percent, 100)


class TestRedactedNames(unittest.TestCase):
    def test_basic(self):
        filename = "Project_Redacted_Name.xlsx"
        shutil.copyfile(f"Example_Exports/{filename}", f"./{filename}")

        myReader = RIS.ExcelReader(filename, verbose=False)
        myProject = myReader.get_data_object()

        self.assertEqual(len(myProject.roles), 2)

        self.assertEqual(myProject.roles[0].label, "Researcher (XX)")
        self.assertEqual(myProject.roles[1].label, "Technician (XX)")

        self.assertEqual(myProject.named_roles, 0)

    def test_name_in_title(self):
        filename = "NameInTitle.xlsx"
        shutil.copyfile(f"Example_Exports/{filename}", f"./{filename}")

        myReader = RIS.ExcelReader(filename, verbose=False)
        myProject = myReader.get_data_object()

        self.assertEqual(myProject.title, "Future Leaders Fellowship  Nano Chemistry")




unittest.main(argv=["first-arg-is-ignored"], exit=False)



