#!/usr/bin/env python
#-*-coding: utf-8 -*-

import unittest
import sys

sys.path.append('..')
from hdfs_util import *

class TestHdfsUtil(unittest.TestCase):
    
    @classmethod
    def setUPClass(self):
        self.hdfs = Hdfs()

    @classmethod
    def 
