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

import math
import pandas as pd
from pathlib import Path
from colorist import Color
import RIS_to_jobs as RIS

class MailMergeCorrector:
    def __init__(self, MailMerge_xlsx='', Teams_csv='', verbose=True, write_output=True):

        self._verbose = verbose
        self._write_output = write_output
        self._True_df  = None
        self._MailMerge_df = None

        self._load_files(MailMerge_xlsx, Teams_csv)
        self._check_MailMerge_for_missing_approval_emails()
        self._check_all_MailMerge_titles_in_Teams()
        self._double_pass_of_correction_loop()
        self._write_file()

    def _load_files(self, MailMerge_xlsx, Teams_csv):
        _check_xlsx_file_extension(MailMerge_xlsx)
        _check_csv_file_extension(Teams_csv)
        self._True_df  = pd.read_csv(Teams_csv)
        self._MailMerge_df = pd.read_excel(MailMerge_xlsx)
        self._MailMerge_df['Outcome'] = self._MailMerge_df['Outcome'].astype('string').fillna('')

    def _check_MailMerge_for_missing_approval_emails(self):
        missing = self._MailMerge_df["Approval ID"][self._MailMerge_df["Approval ID"].isnull()].index.tolist()
        if len(missing)>0 and self._verbose: # pragma: no cover
            exception_message = f"\033[1m{Color.BLACK}The following projects are missing and Approval ID in the Mail Merge Excel file, suggesting the PI email has not been sent.\n{Color.RED}{self._MailMerge_df['Project Title'][missing].to_string(index=False)}\033[0m{Color.BLACK}"
            #raise Exception(exception_message)
            print(exception_message)
            print("These will be treated as reject\n\n")

    def _check_all_MailMerge_titles_in_Teams(self):
        for _,element in self._MailMerge_df.iterrows():
            search_title = f'Action required - Approval for: {element["Project Title"]}'

            match_indexes = self._True_df.index[self._True_df['Title'].eq(search_title)]

            if len(match_indexes) == 0: # pragma: no cover
                print(f"Title {search_title} from MailMerge not found in Teams data")
                raise Exception(f"Title {search_title} from MailMerge not found in Teams data")
        if self._verbose:# pragma: no cover
          print("**** All MailMerge titles found in Teams data ****\n")

    def _double_pass_of_correction_loop(self):
        self._correction_loop()
        if self._verbose: # pragma: no cover
          print("**** All corrections applied ****\n")
          print('Running again to check that no corrections are needed...')
        after_pass1_version = self._MailMerge_df.copy()
        self._correction_loop()
        assert self._MailMerge_df.equals(after_pass1_version) , "Double pass failed"

    def _correction_loop(self):
        for _,element in self._True_df.iterrows():
            search_title = _clean_title(element)

            match_indexes = self._MailMerge_df.index[self._MailMerge_df['Project Title'].eq(search_title)]
            if len(match_indexes) == 0:
              continue
            self._catch_too_many_matches(match_indexes)

            match_index = match_indexes[0]
            assert self._MailMerge_df['Project Title'].iloc[match_index] == search_title, f"Expected title {search_title} at index {match_index}, but found {self._MailMerge_df['Project Title'].iloc[match_index]}"

            correct_response = clean_response(element['Stage'])
            if type(self._MailMerge_df['Approval ID'].iloc[match_index]) is not str:
                correct_response = 'Reject'

            current_response = self._MailMerge_df['Outcome'].iloc[match_index]
            if needs_to_be_corrected(correct_response, current_response):
                self._apply_correction(match_index, correct_response)

    def _catch_too_many_matches(self, match_indexes):
        if len(match_indexes) > 1: # pragma: no cover
            print("Multiple matches found for title:")
            for match_index in match_indexes:
                print(self._MailMerge_df['Project Title'].iloc[match_index])
            raise Exception(f"Expected zero or one match expected, but found {len(match_indexes)}")

    def _apply_correction(self, match_index, correct_response):
        current_response = self._MailMerge_df['Outcome'].iloc[match_index]
        self._MailMerge_df.loc[match_index, 'Outcome'] = correct_response
        if self._verbose: # pragma: no cover
          print(self._MailMerge_df['Project Title'].iloc[match_index])
          print(f"(Correct: {correct_response}, Current: {current_response})")
          print(f"==== Corrected to {correct_response} ====")
          print()

    def _write_file(self):
        filename = 'Mail_Merge_PI_Response.xlsx'
        if self._write_output:
          if Path(filename).exists():
              raise Exception(f"File {filename} already exists. Please move or delete it before running this script.")
          RIS.write_df_to_excel_table(self._MailMerge_df, filename)
        elif self._verbose: # pragma: no cover
          print(f"**** Skipping writing output to {filename} ****\n")



def needs_to_be_corrected( correct_response, current_response ):
    assert current_response in ['Reject', 'Proceed', 'Anonymise', ''], f"Current response '{current_response}' is not one of the expected values"
    assert correct_response in ['Reject', 'Proceed', 'Anonymise', ''], f"Correct response '{correct_response}' is not one of the expected values"
    if correct_response == current_response:
        return False
    assert current_response == '' , f"Response needs corrected, but only blank responses should be over-ridden, but got correct_response='{correct_response}' and current_response='{current_response}'"
    return True


def clean_response( response ):
    if isinstance(response, float) and math.isnan(response):
        return ''

    for option in ['Reject', 'Proceed', 'Anonymise']:
        if response.split(' | ')[-1] == option:
            return option

        if response.split(' | ')[-2] == option:
            return option

    raise Exception(f"Response {response} does not match any of the expected cases")


def _clean_title(element):
    return element.Title.removeprefix('Action required - Approval for: ')

def _check_xlsx_file_extension(MailMerge_xlsx):
    if not MailMerge_xlsx.split('.')[-1] == 'xlsx':
        raise Exception("MailMerge_xlsx must be a .xlsx file")

def _check_csv_file_extension(Teams_csv):
    if not Teams_csv.split('.')[-1] == 'csv':
        raise Exception("Teams_csv must be a .csv file")