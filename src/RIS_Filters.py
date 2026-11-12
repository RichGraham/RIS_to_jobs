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


JOB_FAMILY_PREFIXES = {
    "R&T": "Research & Teaching",
    "APM": "Administrative, Professional & Managerial",
    "Tech": "Technical Services",
    "Opera": "Operations & Facilities",
    "Clinical": "Clinical",
}

def job_family_filter(grade_in, role_type):
    if role_type.startswith("Technician"):
        return "Technical Services"

    grade = grade_in.replace("Casual ", "")

    for prefix, family in JOB_FAMILY_PREFIXES.items():
        if grade.startswith(prefix):
            return family

    print(f" **** Cannot match grade {grade_in} to a job family ****")  # pragma: no cover
    raise ValueError("Grade does not match any known job family")


def status_filter(status):

    exclude_list = _get_exclude_list()
    if _any_list_element_in_string(exclude_list, status):
        return "Exclude"

    awarded_list = _get_awarded_list()
    if _any_list_element_in_string(awarded_list, status):
         return "Funding Awarded"

    pre_submission_list = _get_pre_submission_list()
    if _any_list_element_in_string(pre_submission_list, status):
        return "Pre-submission"

    submitted_list = _get_submitted_list()
    if _any_list_element_in_string(submitted_list, status):
        return "Submitted to Funder"

    return "Unspecified"

def _any_list_element_in_string(phrase_list, string):
    for phrase in phrase_list:
        if phrase in string:
            return True
    return False

def _get_exclude_list():
    return ["Bid Unsuccessful",
            "Project Closed",
    ]

def _get_awarded_list():
    return ["Project Live","Funding Awarded","Award Setup","Award Acceptance",
    ]

def _get_pre_submission_list():
    return ["Bid Development", "Pre-submission",
    ]

def _get_submitted_list():
    return ["Bid Submission", "Submitted to Funder","Bid Awaiting Response",
    ]
