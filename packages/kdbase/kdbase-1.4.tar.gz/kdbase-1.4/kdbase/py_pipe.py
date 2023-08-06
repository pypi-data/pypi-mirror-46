#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""self-defined pipe based on python.

"""

import os
from subprocess import Popen, PIPE 
import sys
import time


def execute(cmds):
    print >> sys.stderr, 'execute cmds: {}'.format(cmds)

    pipes = [] 
    pipes.append(run_pipe(cmds[0], stdin=sys.stdin, stdout=PIPE))  
    for index, cmd in enumerate(cmds[1:-1], start=1):
        pipes.append(run_pipe(cmd, stdin=pipes[index-1].stdout, stdout=PIPE))
    pipes.append(run_pipe(cmds[-1], stdin=pipes[len(cmds)-2].stdout, 
        stdout=sys.stdout))
    
    while True:
        if failure(pipes):
            return False 
        elif success(pipes): 
            return True 
        time.sleep(1)

def success(pipes):
    for pipe in pipes:
        if pipe.poll() != 0:
            return False
    return True

def failure(pipes):
    for pipe in pipes:
        status = pipe.poll()
        if status:
            print >> sys.stderr, 'pipe pid: [{}], err status: {}'.format(pipe.pid, status)
            return True
    return False 

def run_pipe(cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, 
        shell=True, cwd=None):
    try:
        p = Popen(cmd, stdin=stdin, stdout=stdout, stderr=stderr, 
                shell=shell, cwd=cwd)
        print >> stderr, 'pipe pid:[{}], cmd: [{}] start'.format(p.pid, cmd) 
        return p
    except Exception, e:
        import traceback
        error_msg = traceback.format_exc()
        print >> stderr, error_msg
        return False

def main():
    cmd = sys.argv[1]
    print >> sys.stderr, 'py_pipe cmd: {}'.format(str(cmd))
    cmds = [_.strip() for _ in cmd.split('|')]
    res = execute(cmds)
    print >> sys.stderr, 'py_pipe result: {}'.format(res)
    if res:
        exit(0)
    else:
        exit(-1)

if __name__ == '__main__': 
    main()
