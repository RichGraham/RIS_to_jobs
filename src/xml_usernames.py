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

import xmltodict
import re
from colorist import Color

class XML_Usernames:
    def __init__(self,  xml_filename):
        self._xml_dict = _load_xml_file_usernames('MyProjects.xml')

    def get_PI_name_and_username(self,project_id):
        projects = self._xml_dict["Projects"]["Project"]
        # xmltodict returns a dict instead of a list when there is only one item
        if isinstance(projects, dict):
            projects = [projects]

        for project in projects:
            if str(project.get("ProjectID")) == str(project_id):
                return _parse_project_lead(project.get("ProjectLead"))

        raise KeyError(f"ProjectID '{project_id}' not found")


def _load_xml_file_usernames(filename):
    _check_xml_usernames(filename)
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
    return xml_dict

def _check_xml_usernames(filename):
    if not filename.split('.')[-1] == 'xml':
        raise Exception(f"Filename {filename} must be a .xml file")

def _parse_project_lead(project_lead):
    match = re.match(r"^(.*?)\s*\(([^)]+)\)\s*$", project_lead)

    if not match:
        raise ValueError(
            f"Could not parse project lead string: {project_lead}"
        )

    name = match.group(1).strip()
    username = match.group(2).strip()

    return name, username