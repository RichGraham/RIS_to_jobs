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


class Test_EquivalentWithinRemovedCharacters(unittest.TestCase):
    def test_initial(self):
        self.assertTrue(RIS.equivalent_within_removed_characters(short= "abc", long = "abc"))
        self.assertTrue(RIS.equivalent_within_removed_characters(short= "abc", long = "a b c"))
        self.assertTrue(RIS.equivalent_within_removed_characters(short="abc", long ="a\tb\tc"))
        self.assertTrue(RIS.equivalent_within_removed_characters(short="abc", long ="a\rb\rc"))
        self.assertTrue(RIS.equivalent_within_removed_characters(short="abc", long ="abcd"))
        self.assertFalse(RIS.equivalent_within_removed_characters(short="abc", long ="ab"))
        self.assertFalse(RIS.equivalent_within_removed_characters(short="abc", long ="xyz"))

    def test_actual_cases_true(self):
        self.assertTrue(RIS.equivalent_within_removed_characters(
            long = "Fellowship - John Jones - NIHR",
            short= "Fellowship -  - NIHR" ) )
        self.assertTrue(RIS.equivalent_within_removed_characters(
            long = "Fellowship - John Jones - NIHR",
            short= "Fellowship -  " ) )
        self.assertTrue(RIS.equivalent_within_removed_characters(
            long = "FLF - (Anne Green)",
            short= "FLF - (Anne)" ) )
        self.assertTrue(RIS.equivalent_within_removed_characters(
            long = "FLF - (Anne Green)",
            short= "FLF - ()" ) )
        self.assertTrue(RIS.equivalent_within_removed_characters(
            long = "FLF - (Anne Green)",
            short= "FLF " ) )

    def test_actual_cases_false(self):
        self.assertFalse(RIS.equivalent_within_removed_characters(
            long = "Fellowship - John Jones - NIHR",
            short= " Fellowship -  - NIHR" ) )
        self.assertFalse(RIS.equivalent_within_removed_characters(
            long = "Fellowship - John Jones - NIHR",
            short= "Fellxowship -  " ) )
        self.assertFalse(RIS.equivalent_within_removed_characters(
            long = "FLF - (Anne Green)",
            short= "FLF - (Annie)" ) )
        self.assertFalse(RIS.equivalent_within_removed_characters(
            long = "FLF - (Anne Green)",
            short= "FLF2 - ()" ) )
        self.assertFalse(RIS.equivalent_within_removed_characters(
            long = "FLF - (Anne Green)",
            short= "#FLF " ) )

unittest.main(argv=["first-arg-is-ignored"], exit=False)



