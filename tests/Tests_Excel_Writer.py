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
import unittest

sys.path.append(os.path.expanduser("../") )
sys.path.append(os.path.expanduser("./") )
import RIS_to_jobs as RIS
from test_helpers import compare_excel


class TestBasicWriter(unittest.TestCase):
    def test_blank(self):
        filename = "Dummy.xlsx"
        expected_file = "Database_Uploads/NoJobs.xlsx"
        project = []
        _ = RIS.ExcelWriter( project ,filename=filename, include_role_type=True)

        self.assertTrue(compare_excel(filename, expected_file))

    def test_one_job(self):
        filename = "Dummy.xlsx"
        expected_file = "Database_Uploads/OneJob.xlsx"

        roles=[RIS.Job_DataClass(label="Test 1: German Studies Research Fellow",
                                 role_type="Fellow",
                                 grade="R&T does not specify grade",
                                 start_date=datetime.datetime(2028, 4, 25, 0, 0),
                                 length_in_months=12, fte_percent=100)]


        project = RIS.Project_DataClass(title="this role will entail...",
                                           RIS_ID=124346,
                                           PI_name="Richard Graham",
                                           PI_username="pmzrsg",
                                           lead_unit="CLAS",
                                           status = "Pre-submission",
                                           roles=roles)
        project.anonymous = True

        projects = [project]
        _ = RIS.ExcelWriter( projects ,filename=filename, include_role_type=True)

        self.assertTrue(compare_excel(filename, expected_file))

    def test_two_jobs(self):
        filename = "Dummy.xlsx"
        expected_file = "Database_Uploads/TwoJobs.xlsx"

        roles=[RIS.Job_DataClass(label="Test 1: German Studies Research Fellow",
                                 role_type="Fellow",
                                 grade="R&T <grade specified in RIS>",
                                 start_date=datetime.datetime(2026, 4, 1, 0, 0),
                                 length_in_months=12, fte_percent=100),
            RIS.Job_DataClass(label="Senior Project Manager",
                                 role_type="Project Manager",
                                 grade="APM5",
                                 start_date=datetime.datetime(2026, 5, 5, 0, 0),
                                 length_in_months=24, fte_percent=50),
                                 ]


        project = RIS.Project_DataClass(title="this role will entail...",
                                           RIS_ID="1234",
                                           PI_name="Fiona Frost",
                                           PI_username="Fiona.Frost2",
                                           lead_unit="CLAS",
                                           status = "Pre-submission",
                                           roles=roles)

        projects = [project]
        _ = RIS.ExcelWriter( projects ,filename=filename, include_role_type=True)

        self.assertTrue(compare_excel(filename, expected_file))

    def test_different_status(self):
        filename = "Dummy.xlsx"
        expected_file = "Database_Uploads/ThreeProjects.xlsx"


        projects = []

        roles=[RIS.Job_DataClass(label="German Studies Research Fellow",
                                 role_type="Fellow",
                                 grade="R&T5 Aug2018",
                                 start_date=datetime.datetime(2026, 4, 12, 0, 0),
                                 length_in_months=12, fte_percent=100),
                                 ]
        project = RIS.Project_DataClass(title="German Project",
                                    RIS_ID=1,
                                    PI_name="Bob Smith",
                                    PI_username="pgzbs",
                                    lead_unit="CLAS",
                                    status = "Pre-submission",
                                    roles=roles)
        project.anonymous = True
        projects.append(project)

        roles=[RIS.Job_DataClass(label="Medical School",
                                 role_type="Technician",
                                 grade="Technical Services",
                                 start_date=datetime.datetime(2026, 6, 1, 0, 0),
                                 length_in_months=9, fte_percent=50),
                                 ]
        project = RIS.Project_DataClass(title="Medical Project Title",
                                    RIS_ID=2,
                                    PI_name="Alex Jones",
                                    PI_username="somaj",
                                    lead_unit="Medicine",
                                    status = "Submitted to Funder",
                                    roles=roles)
        projects.append(project)

        roles=[RIS.Job_DataClass(label="General Project Manager",
                                 role_type="Ops Manager",
                                 grade="Operations & Facilities",
                                 start_date=datetime.datetime(2027, 10, 23, 0, 0),
                                 length_in_months=18, fte_percent=100),
                                 ]
        project = RIS.Project_DataClass(title="Geography Research Project Title",
                                    RIS_ID=3,
                                    PI_name="Andi Pitt",
                                    PI_username="pgzap5",
                                    lead_unit="Geography",
                                    status = "Funding Awarded",
                                    roles=roles)
        projects.append(project)

        _ = RIS.ExcelWriter( projects ,filename=filename, include_role_type=True)

        self.assertTrue(compare_excel(filename, expected_file))




unittest.main(argv=["first-arg-is-ignored"], exit=False)



