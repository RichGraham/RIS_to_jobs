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
import pickle
import sys
import unittest

sys.path.append(os.path.expanduser("../") )
import RIS_to_jobs as RIS
import test_helpers

initial_directory = os.getcwd()

class Test_PI_Response(unittest.TestCase):
    def test_initial(self):
        output_pickle = "Projects_PI_response.pickle"
        output_excel = "Database_Entries.xlsx"

        os.chdir(initial_directory)
        os.chdir("PI_Response_Folders/Initial_Test")

        if os.path.exists(output_pickle):
            os.remove(output_pickle)
        if os.path.exists(output_excel):
            os.remove(output_excel)

        _ = RIS.Apply_PI_Response(include_role_type=True, verbose=False)

        with open("expected_projects.pickle", "rb") as file:
            expected_projects = pickle.load(file)
        with open("Projects_PI_response.pickle", "rb") as file:
            actual_projects = pickle.load(file)
        self.assertTrue( actual_projects == expected_projects  )


        os.chdir(initial_directory)

    def test_second(self):
        output_pickle = "Projects_PI_response.pickle"
        output_excel = "Database_Entries.xlsx"

        os.chdir(initial_directory)
        os.chdir("PI_Response_Folders/Second_Test")

        if os.path.exists(output_pickle):
            os.remove(output_pickle)
        if os.path.exists(output_excel):
            os.remove(output_excel)

        _ = RIS.Apply_PI_Response(include_role_type=True, verbose=False)

        with open("expected_projects.pickle", "rb") as file:
            expected_projects = pickle.load(file)
        with open("Projects_PI_response.pickle", "rb") as file:
            actual_projects = pickle.load(file)

        self.assertTrue( actual_projects == expected_projects  )
        self.assertTrue( test_helpers.compare_excel(output_excel, "expected_Database_Entries.xlsx") )
        os.chdir(initial_directory)

    def test_second_no_keywords_column(self):
        output_pickle = "Projects_PI_response.pickle"
        output_excel = "Database_Entries.xlsx"

        os.chdir(initial_directory)
        os.chdir("PI_Response_Folders/Second_Test")

        if os.path.exists(output_pickle):
            os.remove(output_pickle)
        if os.path.exists(output_excel):
            os.remove(output_excel)

        _ = RIS.Apply_PI_Response(include_role_type=True, delete_keywords=True,verbose=False)

        with open("expected_projects.pickle", "rb") as file:
            expected_projects = pickle.load(file)
        with open("Projects_PI_response.pickle", "rb") as file:
            actual_projects = pickle.load(file)

        self.assertTrue( actual_projects == expected_projects  )
        self.assertTrue( test_helpers.compare_excel(output_excel, "expected_Database_Entries_no_keywords.xlsx") )
        os.chdir(initial_directory)

    def test_second_no_keywords_column_reject_empty(self):
        output_pickle = "Projects_PI_response.pickle"
        output_excel = "Database_Entries.xlsx"

        os.chdir(initial_directory)
        os.chdir("PI_Response_Folders/Second_Test")

        if os.path.exists(output_pickle):
            os.remove(output_pickle)
        if os.path.exists(output_excel):
            os.remove(output_excel)

        _ = RIS.Apply_PI_Response(include_role_type=True, delete_keywords=True,verbose=False, reject_empty_response=True)

        with open("expected_projects_RejectEmpty.pickle", "rb") as file:
            expected_projects = pickle.load(file)
        with open("Projects_PI_response.pickle", "rb") as file:
            actual_projects = pickle.load(file)

        self.assertTrue( actual_projects == expected_projects  )
        self.assertTrue( test_helpers.compare_excel(output_excel, "expected_Database_Entries_no_keywords_RejectEmpty.xlsx") )
        os.chdir(initial_directory)

    def test_second_no_keywords_column_projects_absent_from_mail_merge(self):
        output_pickle = "Projects_PI_response.pickle"
        output_excel = "Database_Entries.xlsx"

        os.chdir(initial_directory)
        os.chdir("PI_Response_Folders/Second_Test_Missing_MailMerge")

        if os.path.exists(output_pickle):
            os.remove(output_pickle)
        if os.path.exists(output_excel):
            os.remove(output_excel)

        _ = RIS.Apply_PI_Response(include_role_type=True, delete_keywords=True,verbose=False, reject_empty_response=True)

        with open("expected_projects.pickle", "rb") as file:
            expected_projects = pickle.load(file)
        with open("Projects_PI_response.pickle", "rb") as file:
            actual_projects = pickle.load(file)

        #self.assertTrue( actual_projects == expected_projects  )
        self.assertTrue( test_helpers.compare_excel(output_excel, "expected_Database_Entries_no_keywords_absent_projects.xlsx") )
        os.chdir(initial_directory)


    def test_third(self):
        output_excel = "Database_Entries.xlsx"

        os.chdir(initial_directory)
        os.chdir("PI_Response_Folders/Third_Test")

        if os.path.exists(output_excel):
            os.remove(output_excel)

        _ = RIS.Apply_PI_Response(include_role_type=True, verbose=False)

        self.assertTrue( test_helpers.compare_excel(output_excel, "expected_Database_Entries.xlsx") )
        os.chdir(initial_directory)

if __name__ == '__main__':
    unittest.main()


