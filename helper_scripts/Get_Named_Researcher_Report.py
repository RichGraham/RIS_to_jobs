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

from datetime import datetime
import sys
import os
import os.path
import argparse
import pickle
import datetime
from collections import defaultdict

sys.path.append(os.path.expanduser('~/source/RIS_to_jobs/../') )
sys.path.append(os.path.expanduser('~/source/') )
sys.path.append(os.path.expanduser('~/source/RIS_to_jobs') )

import RIS_to_jobs as RIS


def count_roles_from_pickle(file_name = 'Projects.pickle', print_projects = True):
  with open(file_name, 'rb') as f:
    projects = pickle.load(f)

  if print_projects:
    for project in projects:
      print(project)
      print("\n")
    print("\n")

  named_roles = [project.named_roles for project in projects]
  unnamed_roles = [len(project.roles) for project in projects]

  named_roles_count = sum(named_roles)
  unnamed_roles_count = sum(unnamed_roles)
  return named_roles_count, unnamed_roles_count

def count_roles_by_unit(file_name = 'Projects.pickle', print_projects = True):
  with open(file_name, 'rb') as f:
    projects = pickle.load(f)


  if print_projects:
    for project in projects:
      print(project)
      print("\n")
    print("\n")



  counts = defaultdict(lambda: {"named_roles": 0, "unnamed_roles": 0})

  for project in projects:
      counts[project.lead_unit]["named_roles"] += project.named_roles
      counts[project.lead_unit]["unnamed_roles"] += len(project.roles)

  counts = dict(counts)
  sorted_counts = dict(
    sorted(
    counts.items(),
    key=lambda item: item[1]["named_roles"],
    reverse=True
    )
    )

  return sorted_counts


def get_date_from_folder(folder):
  try:
    date = datetime.datetime.strptime(folder, "%b-%d-%Y_%H-%M").date()
  except ValueError:
    print(f"Folder {folder} does not match expected format.")
    return None
  return date

import pandas as pd

def make_summary_report(folders, output_file="named_researcher_summary.xlsx"):
    rows = []

    for folder in folders:
        date = get_date_from_folder(folder)
        named_roles_count, unnamed_roles_count = count_roles_from_pickle(
            f"{folder}/Projects.pickle",
            print_projects=False
        )

        rows.append({
            "Date": date,
            "Named Roles": named_roles_count,
            "Unnamed Roles": unnamed_roles_count
        })

    df = pd.DataFrame(rows)
    df.sort_values("Date", inplace=True)
    df.to_excel(output_file, index=False)
    print(f"Summary report written to {output_file}")

def make_unit_breakdown_report(folders, output_file="named_researcher_lead_unit_breakdown.xlsx"):
  totals = collect_unit_totals(folders)
  write_unit_breakdown_aggregate_to_excel(totals, output_file=output_file)
  print("\n")
  pretty_print_unit_breakdown(totals)

def collect_unit_totals(folders):
  totals = defaultdict(lambda: {"named_roles": 0, "unnamed_roles": 0})
  for folder in folders:
      unit_dictionary = count_roles_by_unit(f"{folder}/Projects.pickle", print_projects=False)
      write_monthly_unit_breakdown_to_excel(unit_dictionary, folder)
      print(f"Unit breakdown report for {folder} written to {folder}/lead_unit_summary.xlsx")

      for unit, counts in unit_dictionary.items():
        totals[unit]["named_roles"] += counts["named_roles"]
        totals[unit]["unnamed_roles"] += counts["unnamed_roles"]

  totals = dict(
       sorted(
        totals.items(),
        key=lambda item: item[1]["named_roles"],
        reverse=True
        )
        )
  return totals


def pretty_print_unit_breakdown(totals):
  print(f"{'Lead Unit':40} {'Named':>8} {'Unnamed':>8}")
  print("-" * 60)

  for unit, counts in totals.items():
      print(
          f"{unit:40} "
          f"{counts['named_roles']:8d} "
          f"{counts['unnamed_roles']:8d}"
      )

def write_unit_breakdown_aggregate_to_excel(totals, output_file= 'lead_unit_summary_aggregate.xlsx'):
  df = pd.DataFrame.from_dict(totals, orient="index")
  df.index.name = "Lead Unit"
  df.reset_index(inplace=True)
  df.columns = ["Lead Unit", "Named Roles", "Unnamed Roles"]
  df.to_excel(output_file, index=False)
  print(f"Unit breakdown aggregate report written to {output_file}")

def write_monthly_unit_breakdown_to_excel(unit_dictionary, folder):
  df = pd.DataFrame.from_dict(unit_dictionary, orient="index")
  df.index.name = "Lead Unit"
  df.reset_index(inplace=True)
  df.to_excel(f"{folder}/lead_unit_summary.xlsx", index=False)

def get_folder_list(file="folder_list.txt"):
  with open(file) as f:
    folders = f.read().splitlines()
  folders = set(folders)  # Remove duplicates
  print(f'Found folders {folders}')
  return folders

if __name__ == "__main__":
  #parser = argparse.ArgumentParser()
  #parser.add_argument('-t', '--test', action='store_true', default=False)
  #args = parser.parse_args()

  folders = get_folder_list()
  make_summary_report(folders)
  make_unit_breakdown_report(folders)
