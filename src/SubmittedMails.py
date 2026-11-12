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
import glob
import os
import pickle
import shutil

import RIS_to_jobs as RIS
from colorist import Color

sent_emails_file = "sent_emails.txt"

opted_out_PIs = []
if os.path.exists("../exclude_PIs.txt"):
    opted_out_PIs = RIS.read_file_to_list("../exclude_PIs.txt")
if os.path.exists("exclude_PIs.txt"):
    opted_out_PIs = opted_out_PIs + RIS.read_file_to_list("exclude_PIs.txt")
opted_out_PIs = list(map(str.lower, opted_out_PIs))


class SubmittedMails:
    def __init__(self, verbose = False):
        self._verbose = verbose
        self._sent_emails_list = list(map(int, [ item for item in RIS.read_file_to_list(sent_emails_file) if not item.startswith('========') ]))
        self._exclude_username_list = []
        if os.path.exists("exclude_PIs.txt"):
            self._exclude_username_list = RIS.read_file_to_list("exclude_PIs.txt") + RIS.opted_out_PIs
        self._folder_name = _get_folder_name()
        self._make_folder()
        self._projects = []
        self._load_projects_count_roles_and_filter_eligible()
        self._create_mail_merge_excel_file()
        self._update_file_of_mails_already_sent()
        with open(f"{self._folder_name}/Projects.pickle", "wb") as file:
            pickle.dump(self._projects, file)

    def _make_folder(self):
        if self._verbose: # pragma: no cover
            print(f"Creating folder {self._folder_name} to store the mail merge file and the list of projects")
        if not os.path.exists(self._folder_name):
            os.makedirs(self._folder_name)

    def _load_projects_count_roles_and_filter_eligible(self):
        for file in glob.glob("./Pro*.xlsx"):
            myReader = RIS.ExcelReader(file, verbose = False, delete_RIS_file=False)
            myProject = myReader.get_data_object()

            if self._is_eligible(myProject):
                self._projects.append(myProject)
                shutil.move(file, self._folder_name)
            else:
                os.remove(file)


    def _is_eligible(self, project):
        if RIS.status_filter( project.status ) != "Submitted to Funder":
            self._print(f"Project {project.RIS_ID} ineligible -  status: {project.status}")
            return False

        if project.RIS_ID in self._sent_emails_list:
            self._print(f"Project {project.RIS_ID} ineligible -  already emailed")
            return False

        if project.PI_username.lower() in {username.lower() for username in self._exclude_username_list}:
            self._print(f"Project {project.RIS_ID} ineligible -  PI username is in exclude list")
            return False

        if len(project.roles) == 0 and project.named_roles == 0:
            self._print(f"Project {project.RIS_ID} ineligible -  no roles (either named or unnamed) found")
            return False

        self._print(f"Project \033[1m{Color.BLACK}{project.RIS_ID} is eligible\033[0m")
        return True

    def _print(self, message):
        if self._verbose: # pragma: no cover
            print(message)

    def _create_mail_merge_excel_file(self):
        if( len(self._projects) > 0):
            RIS.create_email_file([project for project in self._projects if len(project.roles) > 0 ], filename=f"{self._folder_name}/Mail_Merge.xlsx")
            if self._verbose: # pragma: no cover
                named_roles_count = sum([project.named_roles for project in self._projects])
                unnamed_roles_count = sum([len(project.roles) for project in self._projects])
                print(f"Created mail merge file for {len(self._projects)} projects, with {unnamed_roles_count} unnamed roles. Also identified a total of {named_roles_count} named roles")

        else:
            print("No projects eligible for email. No mail merge file created.")

    def _update_file_of_mails_already_sent(self):
        with open(sent_emails_file, "a") as myfile:
            myfile.write(f"======== {self._folder_name} ========\n")
            for project in self._projects:
                myfile.write(str(project.RIS_ID))
                myfile.write("\n")


def _get_folder_name():
    return datetime.datetime.now().strftime("%b-%d-%Y_%H-%M")
