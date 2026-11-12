#!/usr/bin/env python3

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

import sys
import os
import os.path
import argparse
import pandas as pd


sys.path.append(os.path.expanduser('~/source/RIS_to_jobs/../') )
sys.path.append(os.path.expanduser('~/source/') )
sys.path.append(os.path.expanduser('~/source/RIS_to_jobs') )

import RIS_to_jobs as RIS

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', '--print_list', action='store_true', default=False)
  args = parser.parse_args()

  accepted_xml_file = 'FindAcceptedGrants.xml'
  unsuccessful_xml_file = 'FindUnsuccessfulGrants.xml'
  database_snapshot_csv = 'Researcher Transition Support.csv'

  upgrade_list = RIS.Get_Upgrade_List_Just_RIS_ID( accepted_xml_file = accepted_xml_file,
                                       database_snapshot_csv = database_snapshot_csv, catious = True)

  expired_list = RIS.Get_Delete_List_From_Rejected_Just_RIS_ID( rejected_xml_file = unsuccessful_xml_file,
                                      database_snapshot_csv = database_snapshot_csv, catious = True)

  modify_list = pd.concat([upgrade_list, expired_list]).sort_values('RIS ID')

  if args.print_list:
    print(modify_list)

  filename = 'ToChange.xlsx'
  RIS.write_df_to_excel_table( modify_list , filename )
  print(f'Written database updates to file:{filename}')
