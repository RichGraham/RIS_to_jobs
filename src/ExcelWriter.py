
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

import openpyxl

#import itertools
import RIS_to_jobs as RIS

code_path = os.path.dirname(os.path.realpath(__file__))

class ExcelWriter:
    def __init__(self,  projects, filename="Dummy.xlsx", include_role_type=False, delete_keywords=False):
        self.role_counter = 1
        self._include_role_type = include_role_type
        self._initialise_workbook()
        self._write_projects(projects)

        if delete_keywords:
            self.worksheet.delete_cols(4)

        self.workbook.save(filename)



    def _initialise_workbook(self):
        self.workbook = openpyxl.load_workbook(os.path.join(code_path, "../excel/Blank.xlsx"))
        self.worksheet = self.workbook.active

    def _write_projects(self, projects):
        for project in projects:
            self._write_single_project(project)

    def _write_single_project(self, project):
        for role in project.roles:
            self.worksheet.cell(row=self.role_counter+1, column=1).value = project.RIS_ID
            self.worksheet.cell(row=self.role_counter+1, column=2).value = self._get_role_name(role)
            self.worksheet.cell(row=self.role_counter+1, column=3).value = project.title
            self.worksheet.cell(row=self.role_counter+1, column=4).value = project.keywords
            self.worksheet.cell(row=self.role_counter+1, column=5).value = RIS.status_filter(project.status)
            self.worksheet.cell(row=self.role_counter+1, column=6).value = RIS.job_family_filter(role.grade, role.role_type)
            self.worksheet.cell(row=self.role_counter+1, column=7).value = project.lead_unit
            self.worksheet.cell(row=self.role_counter+1, column=8).value = _get_fte_string(role.fte_percent)
            self.worksheet.cell(row=self.role_counter+1, column=9).value = role.fte_percent
            self.worksheet.cell(row=self.role_counter+1, column=10).value = role.length_in_months
            self.worksheet.cell(row=self.role_counter+1, column=11).value = role.start_date.date()
            self.worksheet.cell(row=self.role_counter+1, column=11).number_format = "mm/dd/yyyy;@"
            self.worksheet.cell(row=self.role_counter+1, column=12).value = _get_PI_email_or_anonymous(project)
            self.worksheet.cell(row=self.role_counter+1, column=13).value = f"{project.PI_username}@nottingham.ac.uk"
            self.role_counter += 1

    def _get_role_name(self,role):
        if self._include_role_type:
            return f"{role.role_type}: {role.label}"
        return f"{role.label}"

def _get_PI_email_or_anonymous(project):
        if project.anonymous:
            return "Anonymous"
        return f"{project.PI_username}@nottingham.ac.uk"

def _get_fte_string(fte):
    if fte == 100:
        return "Full Time"
    return "Part Time"
