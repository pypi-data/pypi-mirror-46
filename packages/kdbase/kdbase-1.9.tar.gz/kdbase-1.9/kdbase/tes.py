#!/usr/bin/env python
#-*-coding: utf-8 -*-

import os
import sys

from log import logger

def error(return_obj, msg=''):
    def error_fun(func):
        def wrapper(*args, **kw):
            try:
                return func(*args, **kw)
            except Exception, e:
                a=1
                return a
        return wrapper
    return error_fun
@error
def func(i):
    print i

def tes():
    func(2)
