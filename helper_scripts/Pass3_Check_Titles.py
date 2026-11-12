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
from colorist import Color
from rich.console import Console
from rich.markdown import Markdown


sys.path.append(os.path.expanduser('~/source/RIS_to_jobs/../') )
sys.path.append(os.path.expanduser('~/source/') )
sys.path.append(os.path.expanduser('~/source/RIS_to_jobs') )

import RIS_to_jobs as RIS

def check_for_names(args):

  for filename in args.files_list:
    myReader = RIS.ExcelReader(filename, delete_RIS_file=False, verbose=False)
    myProject = myReader.get_data_object()
    if len(myProject.roles) >0:
      print(f'\033[1m{Color.BLACK}'+f'{myProject.title}'+'\033[0m')


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-x', '--expanded_view', action='store_true', default=False)
  parser.add_argument('-m', '--markdown_view', action='store_true', default=False)
  parser.add_argument('files_list', nargs='+', default=[])
  args = parser.parse_args()

  check_for_names(args)
