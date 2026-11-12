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
import pandas as pd
import unittest
from unittest.mock import patch

sys.path.append(os.path.expanduser("../") )
import RIS_to_jobs as RIS
import test_helpers


class TestGetListToChangeStatusToAccepted(unittest.TestCase):
    def test_initial(self):
        my_cross_ref = RIS.DatabaseCrossReference( accepted_xml_file = 'Upgrade_To_Accepted/accepted_1.xml',
                                           database_snapshot_csv = 'Upgrade_To_Accepted/Database1.csv',
                                           verbose = False)

        expected_output = pd.DataFrame.from_dict({'ID': {0: 11, 1: 22},
                'Project Status': {0: 'Funding Awarded', 1: 'Funding Awarded'}})


        self.assertTrue(test_helpers.compare_data_frames(expected_output, my_cross_ref.correction_list))

    def test_3_roles_in_one_project (self):
        my_cross_ref = RIS.DatabaseCrossReference( accepted_xml_file = 'Upgrade_To_Accepted/accepted_1.xml',
                                           database_snapshot_csv = 'Upgrade_To_Accepted/Database2.csv',
                                           verbose = False)

        expected_output = pd.DataFrame.from_dict({'ID': {0: 11, 1: 22, 2:23,3:24},
                'Project Status': {0: 'Funding Awarded', 1: 'Funding Awarded', 2: 'Funding Awarded', 3: 'Funding Awarded'}})


        self.assertTrue(test_helpers.compare_data_frames(expected_output, my_cross_ref.correction_list))


    def test_redacted_name_in_middle (self):
        my_cross_ref = RIS.DatabaseCrossReference( accepted_xml_file = 'Upgrade_To_Accepted/accepted_name_redacted.xml',
                                           database_snapshot_csv = 'Upgrade_To_Accepted/Database_name_redacted.csv',
                                           verbose = False)

        expected_output = pd.DataFrame.from_dict({'ID': {0: 11, 1: 22},
                'Project Status': {0: 'Funding Awarded', 1: 'Funding Awarded'}})


        self.assertTrue(test_helpers.compare_data_frames(expected_output, my_cross_ref.correction_list))

    @patch('builtins.input', return_value='yes') #Mock the input function to always return 'yes'
    def test_redacted_name_in_middle_and_title_changed_user_says_yes (self, input):
        my_cross_ref = RIS.DatabaseCrossReference( accepted_xml_file = 'Upgrade_To_Accepted/accepted_name_redacted_and_title_change.xml',
                                           database_snapshot_csv = 'Upgrade_To_Accepted/Database_name_redacted.csv',
                                           verbose = False)

        expected_output = pd.DataFrame.from_dict({'ID': {0: 11, 1: 22},
                'Project Status': {0: 'Funding Awarded', 1: 'Funding Awarded'}})


        self.assertTrue(test_helpers.compare_data_frames(expected_output, my_cross_ref.correction_list))


    def test_project_already_listed_as_accepted(self):
        my_cross_ref = RIS.DatabaseCrossReference( accepted_xml_file = 'Upgrade_To_Accepted/accepted_1.xml',
                                           database_snapshot_csv = 'Upgrade_To_Accepted/Database2_Accepted.csv',
                                           verbose = False)

        expected_output = pd.DataFrame.from_dict({'ID': {0: 11},
                'Project Status': {0: 'Funding Awarded'}})


        self.assertTrue(test_helpers.compare_data_frames(expected_output, my_cross_ref.correction_list))

class Test_Get_Delete_List_From_Rejected(unittest.TestCase):
    def test_initial(self):
        my_cross_ref = RIS.Get_Delete_List_From_Rejected( rejected_xml_file = 'Upgrade_To_Accepted/rejected_1.xml',
                                           database_snapshot_csv = 'Upgrade_To_Accepted/Database1.csv',
                                           verbose = False)

        expected_output = pd.DataFrame.from_dict({'ID': {0: 11, 1: 22},
                'Project Status': {0: 'Expired', 1: 'Expired'}})


        self.assertTrue(test_helpers.compare_data_frames(expected_output, my_cross_ref.correction_list))

class TestGetListToChangeStatusToAccepted_Just_RIS_ID(unittest.TestCase):
    def test_initial(self):
        upgrade_list = RIS.Get_Upgrade_List_Just_RIS_ID( accepted_xml_file = 'Upgrade_To_Accepted/accepted_1.xml',
                                           database_snapshot_csv = 'Upgrade_To_Accepted/Database1.csv',
                                           verbose = False)

        expected_output = pd.DataFrame.from_dict({'RIS ID': {0: 10, 1: 20},
                'Project Status': {0: 'Funding Awarded', 1: 'Funding Awarded'}})

        self.assertTrue(test_helpers.compare_data_frames(expected_output, upgrade_list))

    def test_3_roles_in_one_project (self):
        upgrade_list = RIS.Get_Upgrade_List_Just_RIS_ID( accepted_xml_file = 'Upgrade_To_Accepted/accepted_1.xml',
                                           database_snapshot_csv = 'Upgrade_To_Accepted/Database2.csv',
                                           verbose = False)

        expected_output = pd.DataFrame.from_dict({'RIS ID': {0: 10, 1: 20},
                'Project Status': {0: 'Funding Awarded', 1: 'Funding Awarded'}})

        self.assertTrue(test_helpers.compare_data_frames(expected_output, upgrade_list))


    def test_project_already_listed_as_accepted(self):
        upgrade_list = RIS.Get_Upgrade_List_Just_RIS_ID( accepted_xml_file = 'Upgrade_To_Accepted/accepted_1.xml',
                                           database_snapshot_csv = 'Upgrade_To_Accepted/Database2_Accepted.csv',
                                           verbose = False)

        expected_output = pd.DataFrame.from_dict({'RIS ID': {0: 10},
                'Project Status': {0: 'Funding Awarded'}})

        self.assertTrue(test_helpers.compare_data_frames(expected_output, upgrade_list))

class Test_Get_Delete_List_From_Rejected_Just_RIS_ID(unittest.TestCase):
    def test_initial(self):
        expired_list = RIS.Get_Delete_List_From_Rejected_Just_RIS_ID( rejected_xml_file = 'Upgrade_To_Accepted/rejected_1.xml',
                                           database_snapshot_csv = 'Upgrade_To_Accepted/Database1.csv',
                                           verbose = False)

        expected_output = pd.DataFrame.from_dict({'RIS ID': {0: 10, 1: 20},
                'Project Status': {0: 'Expired', 1: 'Expired'}})


        self.assertTrue(test_helpers.compare_data_frames(expected_output, expired_list))

unittest.main(argv=["first-arg-is-ignored"], exit=False)



