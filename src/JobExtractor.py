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

import openpyxl
from colorist import Color
import os

import RIS_to_jobs as RIS



_job_data_label_column = 2

code_path = os.path.dirname(os.path.realpath(__file__))
redact_text = RIS.read_file_to_list(code_path+"/../redact.txt")
if os.path.isfile("redact.txt"): # pragma: no cover
    redact_text += RIS.read_file_to_list("redact.txt")

class JobExtractor:
    def __init__(self,  RIS_report, verbose=True):
        self._initialise_workbook(RIS_report)
        self._project_data = RIS.Project_DataClass()
        self._verbose = verbose
        self._jobs_list = []
        self._named_roles = 0
        try:
             self._staff_costs_start_row = self._find_text_row("Staff Costs", range(1,self.worksheet.max_row+11))
        except RuntimeError: # pragma: no cover
            exception_message = f'''
                \033[1m{Color.BLACK}No staff costs section found, so no jobs to extract.
                Check the excel file {Color.RED}{RIS_report}{Color.BLACK},
                if it has no jobs or is completely the wrong format then remove it from this batch. \033[0m
                '''
            raise Exception(exception_message)
        else:
          self._extract_jobs()

    def get_jobs_list(self):
        return self._jobs_list

    def count_named_roles(self):
        return self._named_roles



    def _initialise_workbook(self, filename):
        self.workbook = openpyxl.load_workbook(filename)
        self.worksheet = self.workbook.active

    def _extract_jobs(self):
        self._job_locations = self._find_job_location_ranges()
        jobs = [self._get_individual_job_data(job_range) for job_range in self._job_locations]

        for job in jobs:
            if RIS.count_names(job.label) ==0 :
                self._jobs_list.append(job)
            else:
                if "teaching" not in job.label.lower():
                    self._named_roles += 1
                if self._verbose:
                    self._screen_output( job )


    def _get_individual_job_data(self, job_range):
        job = RIS.Job_DataClass()

        job.label = self._get_cell_entry("Staff Member Name", job_range)
        for sub_string in redact_text:
            job.label = job.label.replace(sub_string, "XX")

        job.role_type = self._get_cell_entry("Role", job_range)
        job.grade = self._get_cell_entry("Grade & Spinal Point", job_range)
        job.start_date = self._get_cell_entry("Start Date of Post", job_range)
        job.length_in_months = int(self._get_cell_entry("Months On Project", job_range))
        job.fte_percent = int(100*self._get_cell_entry("Percentage Time on Project", job_range))
        return job



    def _get_cell_entry(self, search_text, row_range):
        row = self._find_text_row(search_text, row_range)
        return self.worksheet.cell(row=row,column= _job_data_label_column+1).value

    def _find_job_location_ranges(self, search_text="Directly Incurred"):
        job_locations = []
        for row in range(self._staff_costs_start_row ,self.worksheet.max_row+11):
            for column in range(_job_data_label_column-1, _job_data_label_column+2):
                read_text = self.worksheet.cell(row=row,column=column).value

                if read_text == search_text:
                    job_locations.append((row,column))
                    assert column == 3
                    # Add a check that diagonally down and left cell says 'Staff Member Name'

        job_locations.append((self.worksheet.max_row+10, _job_data_label_column))
        return [ range((job_locations[i])[0], (job_locations[i+1])[0]-1) for i in range(len(job_locations)-1) ]

    def _find_text_row(self, search_text , row_range):
        for row in row_range:
            read_text = self.worksheet.cell(row=row,column= _job_data_label_column ).value
            if read_text == search_text:
                return row

        print(search_text) # pragma: no cover
        raise RuntimeError("Cant find requested text!!!") # pragma: no cover

    def _screen_output(self, job):
        names = RIS.get_names(job.label)
        print(f"\033[1m{Color.BLACK}{job.label}\033[0m contains a name - skipping ")
        if len(names) > 0:
            print(f"I think the name is: {names}.")
        else:
            print("Name found in list of real names (either real_names.txt or from pre-exisiting list with code)")

