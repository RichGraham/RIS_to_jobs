import xmltodict
import re
from colorist import Color

class XML_Usernames:
    def __init__(self,  xml_filename):
        self._xml_dict = _load_xml_file_usernames('MyProjects.xml')

    def get_project_lead_username(self,project_id):
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