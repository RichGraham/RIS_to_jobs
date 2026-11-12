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
import filecmp
import os
import os.path
import re
import shutil
import sys
import unittest
import pickle
import time_machine

sys.path.append(os.path.expanduser("../") )
sys.path.append(os.path.expanduser("./") )
import RIS_to_jobs as RIS
from test_helpers import compare_excel

sent_emails_file = "sent_emails.txt"

class Test_MailMergeCreate(unittest.TestCase):
    def test_initial(self):
        shutil.copy("Example_Exports/Project57324957EPSRCexample_submitted.xlsx", "./")
        shutil.copy(f"controller_files/{sent_emails_file}", "./")
        expected_folder = "Feb-20-2026_10-21"
        if os.path.exists(expected_folder):
            shutil.rmtree(expected_folder)

        with time_machine.travel(datetime.datetime(2026, 2, 20, 10, 21, 0)):
            _ = RIS.SubmittedMails()

        self.assertTrue( os.path.exists(expected_folder)  )
        self.assertTrue( filecmp.cmp(sent_emails_file, "controller_files/expected_files/test_initial.txt" ) )
        self.assertEqual( os.listdir(expected_folder).sort(), ["Projects.pickle","Project57324957EPSRCexample_submitted.xlsx", "Mail_Merge.xlsx"].sort() )
        self.assertEqual( 0, len([element for element in os.listdir("./")  if bool(re.match(r"Project.*.xlsx", element)) ]))
        self.assertTrue( filecmp.cmp(expected_folder + "/Projects.pickle", "controller_files/expected_files/test_initial.pickle" ) )

    def test_two_projects(self):
        for file in [   "Example_Exports/Project57324957EPSRCexample_submitted.xlsx",
                        "Example_Exports/ProjectSecondExample_submitted.xlsx"]:
            shutil.copy(file, "./")
        shutil.copy(f"controller_files/{sent_emails_file}", "./")
        expected_folder = "Feb-20-2026_10-21"
        if os.path.exists(expected_folder):
            shutil.rmtree(expected_folder)

        with time_machine.travel(datetime.datetime(2026, 2, 20, 10, 21, 0)):
            _ = RIS.SubmittedMails()

        self.assertTrue( os.path.exists(expected_folder)  )
        self.assertTrue( filecmp.cmp(sent_emails_file, "controller_files/expected_files/test_two_projects.txt" ) )
        self.assertEqual( os.listdir(expected_folder).sort(), ["Projects.pickle","Project57324957EPSRCexample_submitted.xlsx", "ProjectSecondExample_submitted.xlsx", "Mail_Merge.xlsx"].sort() )
        self.assertEqual( 0, len([element for element in os.listdir("./")  if bool(re.match(r"Project.*.xlsx", element)) ]))
        self.assertTrue( filecmp.cmp(expected_folder + "/Projects.pickle", "controller_files/expected_files/test_two_projects.pickle" ) )

    def test_three_projects(self):
        for file in [   "Example_Exports/Project57324957EPSRCexample_submitted.xlsx",
                        "Example_Exports/ProjectSecondExample_submitted.xlsx",
                        "Example_Exports/ProjectSecondExample.xlsx"]:
            shutil.copy(file, "./")
        shutil.copy(f"controller_files/{sent_emails_file}", "./")
        expected_folder = "Feb-20-2026_10-21"
        if os.path.exists(expected_folder):
            shutil.rmtree(expected_folder)

        with time_machine.travel(datetime.datetime(2026, 2, 20, 10, 21, 0)):
            _ = RIS.SubmittedMails()

        self.assertTrue( os.path.exists(expected_folder)  )
        self.assertTrue( filecmp.cmp(sent_emails_file, "controller_files/expected_files/test_two_projects.txt" ) )
        self.assertEqual( os.listdir(expected_folder).sort(), ["Projects.pickle","Project57324957EPSRCexample_submitted.xlsx", "ProjectSecondExample_submitted.xlsx", "Mail_Merge.xlsx"].sort() )
        self.assertEqual( 0, len([element for element in os.listdir("./")  if bool(re.match(r"Project.*.xlsx", element)) ]))
        self.assertTrue( filecmp.cmp(expected_folder + "/Projects.pickle", "controller_files/expected_files/test_two_projects.pickle" ) )

    def test_four_projects(self):
        for file in [   "Example_Exports/Project57324957EPSRCexample_submitted.xlsx",
                        "Example_Exports/ProjectSecondExample_submitted.xlsx",
                        "Example_Exports/ProjectSecondExample.xlsx",
                        "Example_Exports/ProjectSecondExample_no_roles.xlsx"]:
            shutil.copy(file, "./")
        shutil.copy(f"controller_files/{sent_emails_file}", "./")
        expected_folder = "Feb-20-2026_10-21"
        if os.path.exists(expected_folder):
            shutil.rmtree(expected_folder)

        with time_machine.travel(datetime.datetime(2026, 2, 20, 10, 21, 0)):
            _ = RIS.SubmittedMails()

        self.assertTrue( os.path.exists(expected_folder)  )
        self.assertTrue( filecmp.cmp(sent_emails_file, "controller_files/expected_files/test_two_projects.txt" ) )
        self.assertEqual( os.listdir(expected_folder).sort(), ["Projects.pickle","Project57324957EPSRCexample_submitted.xlsx", "ProjectSecondExample_submitted.xlsx", "Mail_Merge.xlsx"].sort() )
        self.assertEqual( 0, len([element for element in os.listdir("./")  if bool(re.match(r"Project.*.xlsx", element)) ]))
        self.assertTrue( filecmp.cmp(expected_folder + "/Projects.pickle", "controller_files/expected_files/test_two_projects.pickle" ) )


    def test_five_projects(self):
        for file in [   "Example_Exports/Project57324957EPSRCexample_submitted.xlsx",
                        "Example_Exports/ProjectSecondExample_submitted.xlsx",
                        "Example_Exports/ProjectSecondExample.xlsx",
                        "Example_Exports/ProjectSecondExample_no_roles.xlsx",
                        "Example_Exports/ProjectAlreadyEmailed.xlsx",
                        "Example_Exports/ProjectAllNamed.xlsx"]:
            shutil.copy(file, "./")
        shutil.copy(f"controller_files/{sent_emails_file}", "./")
        expected_folder = "Nov-05-2026_15-31"
        if os.path.exists(expected_folder):
            shutil.rmtree(expected_folder)

        with time_machine.travel(datetime.datetime(2026,11, 5, 15, 31, 0)):
            _ = RIS.SubmittedMails()

        self.assertTrue( os.path.exists(expected_folder)  )
        self.assertTrue( filecmp.cmp(sent_emails_file, "controller_files/expected_files/test_five_projects.txt" ) )
        self.assertEqual( os.listdir(expected_folder).sort(), ["Projects.pickle","Project57324957EPSRCexample_submitted.xlsx", "ProjectSecondExample_submitted.xlsx", "Mail_Merge.xlsx"].sort() )
        self.assertEqual( 0, len([element for element in os.listdir("./")  if bool(re.match(r"Project.*.xlsx", element)) ]))
        self.assertTrue( filecmp.cmp(expected_folder + "/Projects.pickle", "controller_files/expected_files/test_five_projects.pickle" ) )
        self.assertTrue(compare_excel(expected_folder + "/Mail_Merge.xlsx", "controller_files/expected_files/Mail_Mege_5_projects.xlsx" ) )

    def test_exclude_PI(self):
        for file in [   "Example_Exports/Project57324957EPSRCexample_submitted.xlsx",
                        "Example_Exports/ProjectSecondExample_submitted.xlsx",
                        "Example_Exports/ProjectSecondExample.xlsx",
                        "Example_Exports/ProjectSecondExample_no_roles.xlsx",
                        "Example_Exports/ProjectAlreadyEmailed.xlsx",
                        "Example_Exports/ProjectAllNamed.xlsx",
                        "Example_Exports/Project6.xlsx",
                        "Example_Exports/Project7.xlsx",
                        "Example_Exports/Project8.xlsx",
                        ]:
            shutil.copy(file, "./")
        shutil.copy(f"controller_files/{sent_emails_file}", "./")
        shutil.copy(f"controller_files/exclude_PIs.txt", "./")
        expected_folder = "Nov-05-2026_15-31"
        if os.path.exists(expected_folder):
            shutil.rmtree(expected_folder)

        with time_machine.travel(datetime.datetime(2026,11, 5, 15, 31, 0)):
            _ = RIS.SubmittedMails()
        os.remove('exclude_PIs.txt')


        self.assertTrue( os.path.exists(expected_folder)  )
        self.assertTrue( filecmp.cmp(sent_emails_file, "controller_files/expected_files/test_pi_exclude.txt" ) )
        self.assertEqual( sorted(os.listdir(expected_folder)), sorted(["Projects.pickle","Project57324957EPSRCexample_submitted.xlsx", 'ProjectAllNamed.xlsx', "Mail_Merge.xlsx"]))
        self.assertEqual( 0, len([element for element in os.listdir("./")  if bool(re.match(r"Project.*.xlsx", element)) ]))
        self.assertTrue(compare_excel(expected_folder + "/Mail_Merge.xlsx", "controller_files/expected_files/Mail_Merge_Exclude_PI.xlsx" ) )

class Test_Count_Roles(unittest.TestCase):
    def test_all_projects(self):
        for file in [   "Example_Exports/CountNamesExample/Project360.xlsx",
                        "Example_Exports/CountNamesExample/Project504.xlsx",
                        "Example_Exports/CountNamesExample/Project601.xlsx",
                        "Example_Exports/CountNamesExample/ProjectAllNamed.xlsx",
                        ]:
            shutil.copy(file, "./")
        shutil.copy("Example_Exports/CountNamesExample/blank.txt", f"./{sent_emails_file}")
        expected_folder = "Feb-20-2026_10-21"
        if os.path.exists(expected_folder):
            shutil.rmtree(expected_folder)

        with time_machine.travel(datetime.datetime(2026, 2, 20, 10, 21, 0)):
            _ = RIS.SubmittedMails()

        with open(f"{expected_folder}/Projects.pickle", "rb") as input_file:
            loaded = pickle.load(input_file)
        roles = RIS.count_roles(loaded)

        self.assertEqual( roles.named, 7)
        self.assertEqual( roles.unnamed, 12)

    def test_one_project_already_counted(self):
        for file in [   "Example_Exports/CountNamesExample/Project360.xlsx",
                        "Example_Exports/CountNamesExample/Project504.xlsx",
                        "Example_Exports/CountNamesExample/Project601.xlsx",
                        "Example_Exports/CountNamesExample/ProjectAllNamed.xlsx",
                        ]:
            shutil.copy(file, "./")
        shutil.copy("Example_Exports/CountNamesExample/just360.txt", f"./{sent_emails_file}")
        expected_folder = "Feb-20-2026_10-21"
        if os.path.exists(expected_folder):
            shutil.rmtree(expected_folder)

        with time_machine.travel(datetime.datetime(2026, 2, 20, 10, 21, 0)):
            _ = RIS.SubmittedMails()

        with open(f"{expected_folder}/Projects.pickle", "rb") as input_file:
            loaded = pickle.load(input_file)
        roles = RIS.count_roles(loaded)

        self.assertEqual( roles.named, 5)
        self.assertEqual( roles.unnamed, 7)


if __name__ == "__main__":
    unittest.main()
#unittest.main(argv=["first-arg-is-ignored"], exit=False)



