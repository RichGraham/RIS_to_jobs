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
import RIS_to_jobs as RIS
import test_helpers


class TestPrepEmails(unittest.TestCase):
    def test_blank_roles(self):
        filename = "Dummy.xlsx"
        expected_file = "EmailSpreadsheets/Basic_BlankRoles.xlsx"
        projects = _get_projects()

        RIS.create_email_file(projects, filename=filename, markdown_function = blank_markdown)

        self.assertTrue(test_helpers.compare_excel(filename, expected_file))

    def test_complete_roles(self):
        filename = "Dummy.xlsx"
        expected_file = "EmailSpreadsheets/Projects_15March26.xlsx"
        projects = _get_projects()

        RIS.create_email_file(projects, filename=filename)

        self.assertTrue(test_helpers.compare_excel(filename, expected_file))


def blank_markdown(project):
    return ""

def _get_projects():
        roles=[RIS.Job_DataClass(label="MC Research Fellow",
                            role_type="Fellow",
                            grade="R&T does not specify grade",
                            start_date=datetime.datetime(2028, 4, 25, 0, 0),
                            length_in_months=12, fte_percent=100),
        RIS.Job_DataClass(label="Experimental support",
                                    role_type="Technician",
                                    grade="Technical Services",
                                    start_date=datetime.datetime(2026, 6, 1, 0, 0),
                                    length_in_months=9, fte_percent=50),
                                    ]


        project = RIS.Project_DataClass(title="AI for net zero",
                                    RIS_ID=124346,
                                    PI_name="Richard Graham",
                                    PI_username="pmzrsg",
                                    lead_unit="Chemistry",
                                    status = "Submitted to funder",
                                    roles=roles)

        roles=[RIS.Job_DataClass(label="PDRA",
                            role_type="Fellow",
                            grade="R&T ",
                            start_date=datetime.datetime(2027, 3, 2, 0, 0),
                            length_in_months=18, fte_percent=60),
                                    ]


        project2 = RIS.Project_DataClass(title="FIC mk2",
                                    RIS_ID=6,
                                    PI_name="Richard Graham",
                                    PI_username="pmzrsg",
                                    lead_unit="School of Mathematical Sciences",
                                    status = "Submitted to funder",
                                    roles=roles)


        return  [project, project2]

unittest.main(argv=["first-arg-is-ignored"], exit=False)



