#-*- coding:utf-8 -*-
from multiprocessing import Process
from subprocess import Popen,PIPE
import shlex
import os
import time
import sys
sys.path.append('../')
from klog import *
import psutil

class WorkerProcess(object):
    def __init__(self,command_line):
        self.cmd_args = shlex.split(command_line)
        self.pid = os.getpid()
        self.child_pid = None
        self.popen_inst = None
        self.memory = None
        
    def start(self):
        self.popen_inst = Popen(self.cmd_args,stdout = PIPE,stderr = PIPE,shell = False)
        self.child_pid = self.popen_inst.pid
        logger().info('父进程id: %d' % self.pid)
        logger().info('子进程id: %d' % self.child_pid)
        child = psutil.Process(self.child_pid)
        self.memory = child.memory_info().rss
        
        return self.popen_inst
    
    def show(self):
        # while self.popen_inst.poll() is not  None:
        while True:
            time_start = time.time()
            buff = self.popen_inst.stdout.readline()
            print 'spend %f s' % (time.time()-time_start)
            time_start = time.time()
            print buff
            if not buff:
                break
            else:
               logger().info(buff)
    
    def show_err(self):
        # while self.popen_inst.poll() is not  None:
        while True:
            time_start = time.time()
            buff = self.popen_inst.stderr.readline()
            print 'spend %f s' % (time.time()-time_start)
            time_start = time.time()
            print buff
            if not buff:
                break
            else:
               logger().error(buff)
    
    #杀死父进程和子进程
    def kill_all(self,signal):
        result = os.killpg(self.pid,signal)
    
    #只杀死子进程
    def kill(self,signa,signal):
        result = os.kill(self.child_pid,signal)

    #获取子进程的返回值
    def get_child_value(self):
        self.popen_inst.wait()
        value = self.popen_inst.returncode
        return value

    def get_child_memory(self):
        return self.memory


def gen_core(pid):
        #设置coredump文件大小
        coreSize_cmd = 'ulimit -c unlimited'
        Popen(coreSize_cmd,stdout = PIPE,stderr = PIPE,shell = True)
        #查询coredump文件产生位置
        corePath_cmd = 'cat /proc/sys/kernel/core_pattern'
        corePath_inst = Popen(corePath_cmd,stdout = PIPE,stderr = PIPE,shell = True)
        corePath = corePath_inst.stdout.readline()
        logger().info('coredump文件:%s' %corePath)
        coreDump_cmd = 'kill -11 '+str(pid)
        try:
            coreDump_inst = Popen(coreDump_cmd,stdout = PIPE,stderr = PIPE,shell = True)
            coreDump_out = coreDump_inst.stdout.readline()
            logger().info('%s'%coreDump_out)
            logger().info('Segmentation fault (core dumped)')
        except:
            logger().info('Error when generating coredump file')


def test1():
    p = WorkerProcess('python child.py')
    #p = WorkerProcess('python test.py')
    p.start()
    p.show()
    #time.sleep(5)
    print '子进程占用内存大小: %d KB' % p.get_child_memory()
    #p.kill()
    time.sleep(1)
    print '子进程返回值: %s' % p.get_child_value()
    

if __name__ == '__main__':
    test1()
