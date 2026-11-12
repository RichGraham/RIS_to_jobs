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


import pickle

import pandas as pd
import RIS_to_jobs as RIS

_accept_word = "Proceed"

class Apply_PI_Response:
  def __init__(self, projects_pickle =  "Projects.pickle", output_pickle = "Projects_PI_response.pickle",
               PI_excel = "Mail_Merge_PI_Response.xlsx", output_database_file = "Database_Entries.xlsx",
               output_email_file = "PI_email_list.txt",
               verbose=True, include_role_type=False, delete_keywords=False, reject_empty_response=False):

    self._output_pickle = output_pickle
    self._verbose = verbose
    self._reject_empty_response = reject_empty_response
    with open(projects_pickle, "rb") as file:
      self._projects = pickle.load(file)
    with open(PI_excel, "rb") as file:
      self._Responses = pd.read_excel(file, na_filter = False)


    self._check_PI_Response_is_valid_answer()

    self._apply_PI_Response_to_pickle()
    with open(self._output_pickle, "wb") as file:
      pickle.dump(self._projects, file)

    _ = RIS.ExcelWriter( self._projects ,filename=output_database_file, include_role_type=include_role_type, delete_keywords=delete_keywords)

    _extract_PI_email_list(output_database_file, output_email_file=output_email_file)

    if self._verbose:
      print(f"Applied PI responses to {len(self._projects)} projects and saved to {output_database_file}, ready for upload to online database.")
      print(f'Written PI email list to {output_email_file} for sending out emails to PIs.')


  def _check_PI_Response_is_valid_answer(self):
     for response in self._Responses["Outcome"]:
      assert response in [_accept_word, "Reject", "Anonymise", ""], f"Invalid response: {response}. Expected '{_accept_word}', 'Reject', or 'Anonymise'."

  def _apply_PI_Response_to_pickle(self):
    remove_ID_list = [ID
                      for ID, Outcome in zip(self._Responses["RIS ID"], self._Responses["Outcome"])
                      if Outcome == "Reject"]
    empty_response_ID_list = [ID
                              for ID, Outcome in zip(self._Responses["RIS ID"], self._Responses["Outcome"])
                              if Outcome == ""]
    anonymous_list = [ID
                  for ID, Outcome in zip(self._Responses["RIS ID"], self._Responses["Outcome"])
                  if Outcome == "Anonymise"]

    absent_from_mail_merge = self._find_projects_absent_from_mail_merge()
    remove_ID_list.extend(absent_from_mail_merge)

    if self._reject_empty_response:
        remove_ID_list.extend(empty_response_ID_list)
        if self._verbose:
            print(f"Rejecting {len(empty_response_ID_list)} projects with empty PI response.")
            print(sorted(empty_response_ID_list))

    self._projects = [project for project in self._projects if project.RIS_ID not in remove_ID_list]

    for project in self._projects:
        if project.RIS_ID in anonymous_list:
            project.anonymous = True

  def _find_projects_absent_from_mail_merge(self):
    RIS_IDs_in_mail_merge = set(self._Responses["RIS ID"])
    projects_absent_from_mail_merge = [project.RIS_ID for project in self._projects if should_be_in_mail_merge_but_isnt(project, RIS_IDs_in_mail_merge)]
    if self._verbose and len(projects_absent_from_mail_merge) > 0:
      print(f"Warning: {len(projects_absent_from_mail_merge)} project(s) are absent from the mail merge. They will be rejected.")
      for project in self._projects:
        if project.RIS_ID in projects_absent_from_mail_merge:
          print(f"\tProject {project.RIS_ID} ({project.PI_name} - {project.PI_username}) {project.title}  is absent from the mail merge.")
    return projects_absent_from_mail_merge

def should_be_in_mail_merge_but_isnt(project, RIS_IDs_in_mail_merge):
  if project.RIS_ID not in RIS_IDs_in_mail_merge and project.PI_username.lower() not in list(map(str.lower,RIS.opted_out_PIs)):
     if len(project.roles) > 0:
        return True
  return False

def _extract_PI_email_list(database_file, output_email_file = "PI_email_list.txt"):
  df = pd.read_excel(database_file)

  emails = (
      df["PI email (hidden)"]
      .dropna()
      .astype(str)
      .str.strip()
      .drop_duplicates()
  )
  email_list = ";".join(emails)

  with open(output_email_file, "w") as f:
      f.write(email_list)


