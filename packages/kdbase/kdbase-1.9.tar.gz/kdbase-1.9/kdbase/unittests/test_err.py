#!/usr/bin/env python
#-*-coding: utf-8 -*-

import unittest
import sys

sys.path.append('..')
from err import error


@error(0)
def f():
    a = 1
    b = 0
    return a / b


@error(None)
def g():
    a = 1
    b = 0
    return a / b


class Test_err(unittest.TestCase):

    
    def test_error(self):
        self.assertEqual(f(), 0) 
        self.assertIsNone(g()) 


if __name__ == '__main__':
    unittest.main()






