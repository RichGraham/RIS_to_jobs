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



# To run this code, you need to have the spaCy library installed. You can install it using pip:
# pip install -U spacy
# python -m spacy download en_core_web_sm

import os
import os.path
import re
import spacy
import RIS_to_jobs as RIS
from colorist import Color

nlp = spacy.load("en_core_web_sm")

code_path = os.path.dirname(os.path.realpath(__file__))

false_positives = RIS.read_file_to_list(code_path+"/../false_positive_names.txt")
if os.path.isfile("false_positive_names.txt"): # pragma: no cover
    false_positives += RIS.read_file_to_list("false_positive_names.txt")
false_positives.sort(key=len,reverse=True)

real_names = RIS.read_file_to_list(code_path+"/../real_names.txt")
if os.path.isfile("real_names.txt"): # pragma: no cover
    real_names += RIS.read_file_to_list("real_names.txt")
real_names.sort(key=len,reverse=True)

def strip_names(title, verbose=False):
    names = RIS.get_names(title)
    stripped_title = str(title)
    for name in names + real_names:
        cleaned_name = name.rstrip(' ')
        cleaned_name = cleaned_name.lstrip(' ')
        #stripped_title = stripped_title.replace(cleaned_name,'')
        stripped_title = re.sub(cleaned_name,'', stripped_title, flags=re.IGNORECASE)
    #if len(names) > 0 and verbose:# pragma: no cover
    if title != stripped_title and verbose:# pragma: no cover
        print(f"\033[1m{Color.RED}{title}\033[0m contains a name")
        print(f'I think the names are:\033[1m{Color.BLACK} {names}\033[0m')
        print(f'Revised title:\033[1m{Color.BLACK} {stripped_title}\033[0m')
        print()
    if is_empty_or_white_space(stripped_title):
        message = f'The following title was left empty after names were stripped {title}. I think the names are {names}. Fix this either by false positives or by editting the excel file (use the title as a guide to the filename).'
        raise RuntimeError(message)
    return stripped_title

def is_empty_or_white_space(text):
    return not text or not text.strip()

def count_names(text, verbose=False):
    for name in real_names:
        if name.title() in text.title():
            if verbose:# pragma: no cover
                print(f"Found real name: {name}")
            return 1
    return len(get_names(text, verbose=verbose))

def get_names(text, verbose=False):
    actual_text = text.title()
    for name in false_positives:
        actual_text = actual_text.replace(name.title(), "")
    if verbose:# pragma: no cover
        print("Actual text after removing false positives:", actual_text)
    doc2 = nlp(actual_text)
    persons = [ent.text for ent in doc2.ents if ent.label_ == "PERSON" and not(in_false_positives(ent.text))]
    if verbose:# pragma: no cover
        print("Names found:", persons)
    return persons

def in_false_positives( check):
    for name in false_positives:
        if name.title() in check.title():
            return True
    return False

