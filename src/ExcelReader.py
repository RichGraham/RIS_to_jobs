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
import re

import openpyxl
import RIS_to_jobs as RIS
from colorist import Color

_project_data_label_column = 2

xml_file_name = 'RECHURDLEsdownload.xml'

class ExcelReader:
    def __init__(self,  RIS_report, delete_RIS_file = True, verbose = True, print_titles = False, get_username_from_xml = False):

        self._initialise_workbook(RIS_report)
        self._RIS_filename = RIS_report
        self._project_data = RIS.Project_DataClass()
        self._verbose = verbose
        self._print_titles = print_titles
        self._get_username_from_xml = get_username_from_xml


        self._xml_usernames_finder = None
        if self._get_username_from_xml:
            self._xml_usernames_finder = RIS.XML_Usernames('MyProjects.xml')




        myExtractor = RIS.JobExtractor(RIS_report, verbose = self._verbose)

        self._project_data.roles = myExtractor.get_jobs_list()
        self._project_data.named_roles = myExtractor.count_named_roles()
        self._read_data()

        if delete_RIS_file:
            os.remove(RIS_report)
            assert (not(os.path.exists(RIS_report))) #Check RIS file was deleted


    def get_data_object(self):
        return self._project_data


    def _initialise_workbook(self, filename):
        self.workbook = openpyxl.load_workbook(filename)
        self.worksheet = self.workbook.active

    def _read_data(self):
        self._project_data.title = RIS.strip_names(self._get_cell_entry("Project Title"), verbose = False)
        if len(self._project_data.roles) > 0:
            self._project_data.title = RIS.strip_names(self._get_cell_entry("Project Title"), verbose = self._print_titles)
        self._project_data.RIS_ID = int(self._get_cell_entry("Project ID"))
        self._project_data.lead_unit = self._get_cell_entry("Lead Org Unit")
        self._project_data.status = self._get_cell_entry("Status")

        raw_PI_data = self._get_cell_entry("Principal Investigator")
        self._project_data.PI_name = re.sub("[\\(\\[].*?[\\)'\\]]", "", raw_PI_data).title().strip()
        self._project_data.PI_username = re.sub("^.*\\((.*?)\\)[^\\(]*$", "\\g<1>", raw_PI_data)
        if self._get_username_from_xml:
            PI_name, username = self._xml_usernames_finder.get_PI_name_and_username(self._project_data.RIS_ID)
            self._project_data.PI_username = username
            assert PI_name.lower() == self._project_data.PI_name.lower(), f"PI name from XML ({PI_name}) does not match PI name from RIS ({self._project_data.PI_name}"





    def _get_cell_entry(self, search_text):
        row = self._find_project_text_row(search_text)
        return str(self.worksheet.cell(row=row,column= _project_data_label_column+1).value)

    def _find_project_text_row(self, search_text):
        for row in range(1,self.worksheet.max_row+11):
            read_text = self.worksheet.cell(row=row,column= _project_data_label_column ).value
            if read_text == search_text:
                return row

        raise RuntimeError(f"Cant find requested text: {search_text}!!!\n Issue with:\n \033[1m{Color.BLACK}{self._RIS_filename}\033[0m") # pragma: no cover

