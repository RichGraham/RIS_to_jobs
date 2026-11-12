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
import sys

sys.path.append(os.path.expanduser("../") )
import RIS_to_jobs as RIS


def project_markdown( project):
    details = [project_details( project )]
    roles_divider = ["""### Roles\n"""]
    roles_formatted = [role_details(role) for role in project.roles]
    return "".join(details + roles_divider+ roles_formatted)

def project_details( project ):
    output = f"""## {project.title}\n
* PI email: {project.PI_username}@nottingham.ac.uk
* Lead unit: {project.lead_unit}
* Project status: {RIS.status_filter(project.status)}\n"""

    return output

def role_details( role ):
    output = f"""* {role.label}
     - {RIS.job_family_filter(role.grade, role.role_type)}
     - {role.fte_percent}% FTE for {role.length_in_months} months
    - Planned start date: {role.start_date.strftime('%B %Y')}\n"""
    return output
