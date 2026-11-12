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
from tabulate import tabulate


def compare_excel(file1, file2):
    df1 = pd.read_excel(file1, dtype = str, na_filter = False)
    df2 = pd.read_excel(file2, dtype = str, na_filter = False)

    return compare_data_frames(df1, df2)

def compare_data_frames(df1, df2):

    if( df1.shape != df2.shape): # pragma: no cover
        print(tabulate(df1))
        print(df2)
        return False

    if (df1 == df2).all().all():
        return True
    # pragma: no cover
    print(tabulate(df1))
    print(tabulate(df2))
    print(df2.dtypes)
    print(df1.dtypes)
    print(tabulate(df1.eq(df2)))
    print(tabulate(df1.compare(df2)))
    return False
