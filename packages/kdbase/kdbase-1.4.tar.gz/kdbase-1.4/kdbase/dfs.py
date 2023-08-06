#coding=utf-8
import subprocess
hadoopDir='/opt/hadoop-3.1.0/bin/hadoop'
hadoop_cmd_pure=hadoopDir+' fs'
def execute_cmd(cmd):
    p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for line in p.stdout:
        print line.strip()
def ls(path):
    cmd=hadoop_cmd_pure+' -ls '+path
    execute_cmd(cmd)
def get(src_file,dest_file):
    cmd=hadoop_cmd_pure+' -get -f '+src_file+' '+dest_file
    execute_cmd(cmd)
def put(src_file,dest_file):
    cmd=hadoop_cmd_pure+' -put '+src_file+' '+dest_file
    execute_cmd(cmd)

def mkdir(path):
    cmd=hadoop_cmd_pure+' -mkdir '+path
    execute_cmd(cmd)
def rm(path):
    cmd=hadoop_cmd_pure+' -rmr '+path
    execute_cmd(cmd)
def cat(path):
    cmd=hadoop_cmd_pure+' -cat '+path
    execute_cmd(cmd)

def copy(src_file,dest_file):
    cmd=hadoop_cmd_pure+' -copyFromLocal '+src_file+' '+dest_file
    execute_cmd(cmd)

if __name__=='__main__':
    #display the files in this directory or any directory
    ls('/test')
    cat('/test/input/wly/test4')

