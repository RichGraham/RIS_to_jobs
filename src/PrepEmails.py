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

import pandas as pd
import RIS_to_jobs as RIS


def create_email_file( projects, filename="Mail_Merge.xlsx", markdown_function = RIS.project_markdown):
    data = {
        "RIS ID": [project.RIS_ID for project in projects],
        "Project Title": [project.title for project in projects],
        "PI Name": [project.PI_name.split()[0]for project in projects],
        "PI Email": [f"{project.PI_username}@nottingham.ac.uk" for project in projects],
        "Project roles text":[markdown_function(project) for project in projects],
        "Approval ID": [""]*len(projects),
        "Outcome": [""]*len(projects),
    }
    df = pd.DataFrame(data)
    #df.to_excel(filename, index=False)
    write_df_to_excel_table(df, filename)

def write_df_to_excel_table( data, excel_file):
    with pd.ExcelWriter(excel_file, engine="xlsxwriter") as ew:
        sheet_name="Sheet1"
        sheet_df = data
        data.to_excel(ew, sheet_name=sheet_name, index=False)
        worksheet = ew.sheets[sheet_name]
        options = {"columns": [{"header": c} for c in sheet_df.columns]}

        worksheet.add_table(0, 0, data.shape[0], data.shape[1]-1, options=options)
