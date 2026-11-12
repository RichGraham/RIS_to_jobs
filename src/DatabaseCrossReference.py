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


import pandas as pd
import xmltodict
from colorist import Color
import RIS_to_jobs as RIS

accepted_xml_statuses = ['Award Acceptance', 'Project Live','Award Setup', 'Project Setup']
rejected_xml_statuses = ['Bid Unsuccessful', 'Discarded']


def Get_Delete_List_From_Rejected( rejected_xml_file = '', database_snapshot_csv = '', verbose = True, catious=False):
    return DatabaseCrossReference(accepted_xml_file = rejected_xml_file , database_snapshot_csv = database_snapshot_csv, verbose = verbose, xml_statuses=rejected_xml_statuses, catious=catious, new_status='Expired')

def Get_Upgrade_List_Just_RIS_ID(**kwargs):
    my_cross_ref = DatabaseCrossReference( **kwargs)
    return my_cross_ref.get_just_RIS_IDs().sort_values('RIS ID')

def Get_Delete_List_From_Rejected_Just_RIS_ID( rejected_xml_file = '', database_snapshot_csv = '', verbose = True, catious=False):
    my_cross_ref = DatabaseCrossReference(accepted_xml_file = rejected_xml_file , database_snapshot_csv = database_snapshot_csv, verbose = verbose, xml_statuses=rejected_xml_statuses, catious=catious, new_status='Expired')
    return my_cross_ref.get_just_RIS_IDs().sort_values('RIS ID')


class DatabaseCrossReference:
    def __init__(self, accepted_xml_file = '', database_snapshot_csv = '', verbose = True, xml_statuses = accepted_xml_statuses, catious=False, new_status = 'Funding Awarded'):
        self._verbose = verbose
        self._catious = catious
        self._expected_xml_statuses = xml_statuses
        self._new_status = new_status

        self._accepted_grants = self._load_accept_xml(accepted_xml_file)
        self._database_snapshot = self._load_database_snapshot_csv(database_snapshot_csv)
        _correction_list = self._build_correction_list()
        _correction_list['Project Status'] = self._new_status
        self._stored_list = _correction_list
        self.correction_list = self._strip_correction_list(_correction_list).sort_values('ID')


    def _load_accept_xml(self,filename):
        _check_xml(filename)
        with open(filename, 'r', encoding='utf-8') as file:
            my_xml = file.read()
        try:
            xml_dict = xmltodict.parse(my_xml)
        except Exception:
            exception_message=f'''
            \033[1m{Color.BLACK}
            The RIS xml file {Color.RED}{filename}{Color.BLACK} seems to be the wrong format. Check the file and maybe redownload from RIS.
            \033[0m'''
            raise Exception(exception_message)

        final_list = []
        for element in xml_dict['Projects']['Project']:
            if element['Status'] in self._expected_xml_statuses:
                final_list.append(element)
            elif self._verbose:
                print(f"Removed grant: {element['ProjectID']} as status, {element['Status']}, is not in the targetted list.")
                if self._catious:
                    exception_message=f'''
                            \033[1m{Color.BLACK}
            Grant: {Color.RED}{element['ProjectID']}{Color.BLACK} has status: {Color.RED}{element['Status']}{Color.BLACK}, which is not in the targetted list.
            This strongly suggest that your RIS export file is wrong;
            Check your RIS export criteria and then repeat the export
            \033[0m'''
                    raise ValueError(exception_message)
        return final_list

    def _load_database_snapshot_csv(self, filename):
        _check_csv(filename)
        df = pd.read_csv(filename)
        for _, row in df.iterrows():
            if row['Project Status'] not in ['Pre-submission','Submitted to Funder','Funding Awarded']:
                raise ValueError(f'Database csv has incorrect Project Status: ID{row["ID"]} {row["Project Status"]}')

        ignore_string = 'Funding Awarded'
        filter = df['Project Status'].str.contains(ignore_string)
        filtered_df = df[~filter]
        return filtered_df

    def _build_correction_list(self):
        correction_list = self._database_snapshot.iloc[:0].copy()
        for grant in self._accepted_grants:
            matching_df = self._find_all_entries_in_database(int(grant['ProjectID']))
            self._check_consistency(grant, matching_df)
            if self._verbose and len(matching_df) > 0:
                print(f"Grant {grant['ProjectID']} passed consistency checks with {len(matching_df)} matching entries in the database.")
            correction_list = pd.concat([correction_list, matching_df], ignore_index=True, sort=True)
        return correction_list

    def _find_all_entries_in_database(self, RIS_id):
        return self._database_snapshot[self._database_snapshot['RIS ID'] == RIS_id]

    def _check_consistency(self, grant, matching_df):
        if len(matching_df) == 0:
            return
        for _, row in matching_df.iterrows():
            if str(row['RIS ID']) != str(grant['ProjectID']):
                raise ValueError(f"Mismatch in RIS ID for grant {grant['ProjectID']}. Found {row['RIS ID']} in database.")
            if _username_from_email(row['PI Email']) != _username_from_brackets(grant['ProjectLead']) and _username_from_email(row['PI Email']) != 'Anonymous':
                raise ValueError(f"Mismatch in Project Lead for grant {grant['ProjectID']}. Found '{_username_from_email(row['PI Email'])}' in database, expected '{_username_from_brackets(grant['ProjectLead'])}'.")
            self._check_project_title_consistency(grant, row)

    def _check_project_title_consistency(self, grant, row):
        if RIS.equivalent_within_removed_characters( short = row['Description'], long = grant['ProjectTitle']):
            return
        if self._verbose: # pragma: no cover
            print(f"\033[1m Mismatch in Project Title\033[0m for grant {grant['ProjectID']}.\n\tDtBase:\t\033[1m{Color.RED}'{row['Description']}{Color.BLACK}'\033[0m in database,\n\tRIS: \t\033[1m{Color.RED}'{grant['ProjectTitle']}{Color.BLACK}\033[0m'.")

        if UserYesOrNoQuestion("Do you want to accept these titles as the same?"    ):
            if self._verbose: # pragma: no cover
                print("User replied yes so accepting titles are the same")
        else:
            raise ValueError(f"User replied no so quitting whole process - update file not written. To continue, edit the RIS export file to remove the grant {grant['ProjectID']} (this wii leave the database status for this unchanged), then rerun this script.")




    def _strip_correction_list(self, correction_list):
        columns_to_keep = ['ID', 'Project Status']
        return correction_list[columns_to_keep]

    def get_just_RIS_IDs(self):
        data = self._stored_list['RIS ID'].unique()
        return pd.DataFrame({'RIS ID': data,'Project Status': [self._new_status]*len(data)}).sort_values('RIS ID')

def _username_from_email(email):
    return email.split('@')[0]

def _username_from_brackets(name):
    if '(' in name and ')' in name:
        return name.split('(')[1].split(')')[0]
    return None

def _check_xml(filename):
    if not filename.split('.')[-1] == 'xml':
        raise Exception(f"Filename {filename} must be a .xml file")


def _check_csv(filename):
    if not filename.split('.')[-1] == 'csv':
        exception_message=f'''
            \033[1m{Color.BLACK}
            Expected {Color.RED}{filename}{Color.BLACK} to be a .csv file. This should be the database file. Check you downloaded this properly.
            \033[0m'''
        raise Exception(exception_message)

def UserYesOrNoQuestion(Prompt):
    while True:
        user_input = input(f"{Prompt} Please enter (yes/no): ")
        if user_input.lower() in ["yes", "y", "Yes", "Y", "YES"]:
            return True
        elif user_input.lower() in ["no", "n", "No", "N", "NO"]:
            return False
        else:
            print("Invalid input. Please enter yes/no.")