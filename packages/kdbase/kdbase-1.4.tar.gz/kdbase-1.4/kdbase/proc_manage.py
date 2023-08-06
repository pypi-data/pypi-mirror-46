#-*- coding:utf-8 -*-
from multiprocessing import Process
from subprocess import Popen,PIPE
import shlex
import os
import time

class WorkerProcess(object):
    def __init__(self,command_line):
        self.cmd_args=shlex.split(command_line)
    def start(self):
        self.popen_inst= Popen(self.cmd_args,stdout=PIPE,stderr=PIPE,shell=False)
        self.pid=os.getpid()
        self.kid_pid=self.popen_inst.pid
        print '父进程id: %d' % self.pid
        print '子进程id: %d' % self.kid_pid
        return self.popen_inst
    def show(self):
        # while self.popen_inst.poll() is not  None:
        while True:
            buff=self.popen_inst.stdout.readline()
            if not buff:
                break
            else:
                print(buff)
       
    def send_signal(self,signal):
        self.proc_pid=os.getpid()
        resultr=os.killpg(self.proc_pid,signal)
    def kill(self):
        self.send_signal(9)
def generate_coredump(pid):
        #设置coredump文件大小
        coreSize_cmd='ulimit -c unlimited'
        Popen(coreSize_cmd,stdout=PIPE,stderr=PIPE,shell=True)
        #查询coredump文件产生位置
        corePath_cmd='cat /proc/sys/kernel/core_pattern'
        corePath_inst=Popen(corePath_cmd,stdout=PIPE,stderr=PIPE,shell=True)
        corePath=corePath_inst.stdout.readline()
        print 'coredump文件:%s' %corePath
        coreDump_cmd='kill -11 '+str(pid)
        try:
            coreDump_inst=Popen(coreDump_cmd,stdout=PIPE,stderr=PIPE,shell=True)
            coreDump_out=coreDump_inst.stdout.readline()
            print '%s'%coreDump_out
            print 'Segmentation fault (core dumped)'
        except:
            print 'Error when generating coredump file'

def test1():
    p=WorkerProcess('python test_procManage.py')
    #p=WorkerProcess('python test.py')
    p.start()
    p.show()
    time.sleep(5)
    p.kill()
    time.sleep(10)

if __name__=='__main__':

    test1()
