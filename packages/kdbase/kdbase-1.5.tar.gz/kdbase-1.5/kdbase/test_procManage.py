#-*- coding:utf-8 -*-
import os
import time
import sys

if __name__=='__main__':
    for i in range(0,10):
        print '第%d次:子进程id: %d' % (i,os.getpid())
        sys.stdout.flush()
        time.sleep(1)
