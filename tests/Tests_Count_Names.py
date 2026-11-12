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
import os.path
import sys
import unittest

sys.path.append(os.path.expanduser("../") )
import RIS_to_jobs as RIS


class TestCountNames(unittest.TestCase):
    def test_real_names(self):
        expected_names = ["James", "Omar", "Rod Jones", "Isabel", "Isobel",
                        "olive manger", "PDRA - Matthew Appleton", "Project Manger Peter Jones",
                         ]
        for raw_name in expected_names:
            for name in [raw_name, raw_name.lower(), raw_name.upper(), raw_name.title()]:
                self.assertTrue(RIS.count_names(name) > 0, f"Expected {name} to be flagged as a name, but got a count of 0 instead")



    def test_not_really_names(self):
        not_names = ["ROD PDRA", "Project manager", "Project manger", "Rt4A-R",
                        ]

        for raw_name in not_names:
            for name in [raw_name, raw_name.lower(), raw_name.upper(), raw_name.title()]:
                self.assertEqual(RIS.count_names(name), 0, f"Expected {name} to not be found, but got a count instead")

class TestInFalsePositives(unittest.TestCase):
    def test_false_positives(self):
        false_positives = ["Project manger", "Rt4A-R",
                        ]

        for raw_name in false_positives:
            for name in [raw_name, raw_name.lower(), raw_name.upper(), raw_name.title()]:
                self.assertTrue(RIS.in_false_positives(name), f"Expected {name} to be in false positives, but it was not found")

class TestStripsNames(unittest.TestCase):
    def test_strips_names(self):
        inputs_and_outputs = [
            ("Fellow Peter Jones", "Fellow "),
            ("Paul Palmer-Gearrenizenamen NIHR Three Days On", " NIHR Three Days On"),
            ("ANDY WRIGHT Post-Doctoral Fellowship", " Post-Doctoral Fellowship"),
            ('From Bad to Worse: Tools for Co‑designing Generative AI with BLeT', 'From Bad to Worse: Tools for Co‑designing Generative AI with BLeT')
        ]
        for input_str, expected_output in inputs_and_outputs:
            #print(f"Testing input: '{input_str}' with expected output: '{expected_output}: got '{RIS.strip_names(input_str)}'")
            self.assertEqual(RIS.strip_names(input_str), expected_output)

    def test_catch_blank_title(self):
        inputs=['', ' ','            ','Bob Jones','Anna Green']
        for input in inputs:
            #print(RIS.strip_names(input))
            self.assertRaises(RuntimeError,lambda:RIS.strip_names(input))

class TestEmptyOrWhiteSpace(unittest.TestCase):
    def test_basic(self):
        self.assertTrue( RIS.is_empty_or_white_space(''))
        self.assertTrue( RIS.is_empty_or_white_space('     '))
        self.assertTrue( RIS.is_empty_or_white_space(None))

        self.assertFalse( RIS.is_empty_or_white_space('.         '))
        self.assertFalse( RIS.is_empty_or_white_space('      .'))
        self.assertFalse( RIS.is_empty_or_white_space('Project <NAME>'))

unittest.main(argv=["first-arg-is-ignored"], exit=False)



