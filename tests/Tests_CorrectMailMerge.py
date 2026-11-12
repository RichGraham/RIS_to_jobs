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
import math
import unittest

sys.path.append(os.path.expanduser("../") )
import RIS_to_jobs as RIS

import test_helpers

initial_directory = os.getcwd()

class Test_PI_Response(unittest.TestCase):
    def test_initial(self):
      output_excel = "Mail_Merge_PI_Response.xlsx"
      input_excel = "Mail_Merge_Date.xlsx"
      input_teams = "Teams.csv"
      expected_output_excel = "expected_Mail_Merge_PI_Response.xlsx"

      os.chdir(initial_directory)
      os.chdir("MailMergeCorrection_Folders/Initial")
      if os.path.exists(output_excel):
            os.remove(output_excel)

      RIS.MailMergeCorrector( MailMerge_xlsx=input_excel, Teams_csv=input_teams, verbose=False)

      self.assertTrue( test_helpers.compare_excel(output_excel, expected_output_excel) )
      os.chdir(initial_directory)

    def test_second(self):
      output_excel = "Mail_Merge_PI_Response.xlsx"
      input_excel = "Mail_Merge_Date.xlsx"
      input_teams = "Teams.csv"
      expected_output_excel = "expected_Mail_Merge_PI_Response.xlsx"

      os.chdir(initial_directory)
      os.chdir("MailMergeCorrection_Folders/Second")
      if os.path.exists(output_excel):
            os.remove(output_excel)

      RIS.MailMergeCorrector( MailMerge_xlsx=input_excel, Teams_csv=input_teams, verbose=False)

      self.assertTrue( test_helpers.compare_excel(output_excel, expected_output_excel) )
      os.chdir(initial_directory)

class TestCleanResponse(unittest.TestCase):
    def test_clean_response(self):
        inputs_and_outputs = [ (math.nan, ""),
          ("XXX (staff) | 5/6/2026 9:38:32 AM | Reject", "Reject") ,
          ("YYY(staff) | 5/6/2026 9:38:32 AM | Reject | No! Reject this! Do Not Proceed", "Reject") ,
          ("X | 5/6/2026 9:31:34 AM | Anonymise", "Anonymise") ,
          ("Bob | 5/6/2026 9:38:32 AM | Anonymise | Dont reveal my name", "Anonymise") ,
          ("Ian Wills (staff) | 5/6/2026 9:38:32 AM | Proceed", "Proceed") ,
          ("Anne Cleaves (staff) | 5/6/2026 11:51:42 AM | Proceed | Comment: Kindly proceed with listing my project", "Proceed") ,
          ]

        for input, expected_output in inputs_and_outputs:
            self.assertEqual(RIS.clean_response(input), expected_output)

unittest.main(argv=["first-arg-is-ignored"], exit=False)