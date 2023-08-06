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
                import traceback
                error_msg = traceback.format_exc()
                logger().error('error msg: %s, trackback msg: %s', msg, error_msg)
                return return_obj
        return wrapper
    return error_fun


