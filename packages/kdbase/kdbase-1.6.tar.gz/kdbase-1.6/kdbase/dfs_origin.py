#!/usr/bin/env python
#-*-coding: utf-8 -*-

import os
import sys
import json
import math
import traceback
import urllib2
from pyhdfs import HdfsClient

import dodge_path
from err import error
from log import logger
import service_config as config

hadoop_namenode1 = config.GET_CONF('hadoop', 'hadoop_namenode1')
hadoop_namenode2 = config.GET_CONF('hadoop', 'hadoop_namenode2')

hadoop_home = config.GET_CONF('hadoop', 'hadoop_home')

client = HdfsClient(
    hosts = '%s:50070,%s:50070'%(hadoop_namenode1, hadoop_namenode2),
    user_name = 'hadoop')

@error(None)
def listdir(hdfs_path):
    return client.listdir(hdfs_path)

@error(False)
def mkdirs(hdfs_path):
    return client.mkdirs(hdfs_path)

def exists(hdfs_path):
    return client.exists(hdfs_path)

@error(False)
def create_file(hdfs_path, data, overwrite = True):
    client.create(path=hdfs_path, data=data, overwrite=overwrite)
    return True

@error(False)
def append(hdfs_path, data):
    client.append(hdfs_path, data)
    return True

@error(None)
def get_file_checksum(hdfs_path):
    return client.get_file_checksum(hdfs_path).bytes[:-8]

@error(False)
def delete(hdfs_path):
    res = False
    if exists(hdfs_path):
        res = client.delete(hdfs_path, recursive = True)
    else:
        logger().info('del target file[%s] not exists' % hdfs_path)
        return True
    return res

@error(False)
def set_xattr(path, xattr_name, xattr_value, flag):
    client.set_xattr(path, xattr_name, xattr_value, flag)
    return True

@error(False)
def get_xattr(path, xattr_name):
    return client.get_xattrs(path, xattr_name)

@error(None)
def list_xattrs(path):
    return client.list_xattrs(path)

@error(None)
def get_active_namenode():
    return client.get_active_namenode()

@error(None)
def get_file_status(hdfs_path):
    file_status = client.get_file_status(hdfs_path)
    time = file_status.modificationTime
    return (hdfs_path, time)

@error(None)
def get_content_sum(hdfs_path):
    '''
    return ContentSummary

    spaceQuota（int） - 磁盘空间配额
    fileCount（int） - 文件数
    quota（int） - 此目录的命名空间配额
    directoryCount（int） - 目录数
    spaceConsumed（int） - 内容占用的磁盘空间
    length（int） - 内容使用的字节数

    '''
    cs = client.get_content_summary(hdfs_path)
    content = {}
    content['spaceQuota'] = cs.spaceQuota
    content['fileCount'] = cs.fileCount
    content['quota'] = cs.quota
    content['directoryCount'] = cs.directoryCount
    content['spaceConsumed'] = cs.spaceConsumed
    content['length'] = cs.length

    return content

def download_native(hdfs_path, local_path):
    cmd = '%s/bin/hadoop fs -get -f %s %s' % (
            hadoop_home, hdfs_path, local_path)
    code = os.system(cmd)
    return code == 0

def download_py(hdfs_path, local_path):
    client.copy_to_local(hdfs_path, local_path)
    hdfs_file_size = get_content_sum(hdfs_path)['length']
    local_file_size = os.path.getsize(local_path)
    logger().info('hdfs_file_size[%s] vs local_file_size[%s]', 
            hdfs_file_size, local_file_size)
    assert hdfs_file_size == local_file_size, 'file sizes different'
    return True

def download(hdfs_path, local_path, retry_time=3):
    if not exists(hdfs_path):
        logger().error('hdfs_path:%s not exists' % (hdfs_path))
        return False
    file_name = hdfs_path.split('/')[-1]
    local_file_path = '%s/%s_test'%(local_path, file_name)
    logger().info('download hdfs_path[%s], local_path[%s]',
            hdfs_path, local_file_path)
    try:
        i = 1/ 0
        return download_py(hdfs_path, local_file_path)
    except Exception, e:
        if retry_time == -1:
            return False
        error_msg = traceback.format_exc()
        logger().error('download faill error:%s' % (error_msg))
        res = download_native(hdfs_path, local_file_path)
        if res:
            logger().info('native download success')
            return True
        return download(hdfs_path, local_path, retry_time - 1)

@error(False)
def download_dir(hdfs_path, local_path):
    if not client.exists(hdfs_path):
        logger().error('hdfs_path:%s not exists'%(hdfs_path))
        return False
    if hdfs_path[-1] == os.sep:
        hdfs_path = hdfs_path[:-1]
    if local_path[-1] == os.sep:
        local_path = local_path[:-1]
    target_dir = hdfs_path.split(os.sep)[-1]
    dir_tree = client.walk(hdfs_path)
    for root, dirs, files in dir_tree:
        for file in files:
            path_element = root.split(os.sep)
            append_path = target_dir
            if path_element[-1] != target_dir:
                index = path_element.index(target_dir)
                append_path = os.sep.join(path_element[index:])
            local_path_tmp = local_path +os.sep + append_path
            if not os.path.exists(local_path_tmp):
                os.makedirs(local_path_tmp)
            hdfs_file_path = root + os.sep + file
            res = download(hdfs_file_path, local_path_tmp)
            if not res:
                delete(local_path)
                del_path = local_path + os.sep + target_dir
                for root, dirs, files in os.walk(del_path):
                    for file in files:
                        os.remove(os.path.join(root, file))
                    for dir in dirs:
                        os.rmdir(os.path.join(root, file))
                return False
    return True

def upload(local_path, hdfs_path, retry_time = 3):
    if not os.path.exists(local_path):                                                                                            
        logger().error('local_path:%s not exists'%(local_path))
        return False
    file_name = local_path.split('/')[-1]
    hdfs_path = '%s/%s'%(hdfs_path, file_name)
    logger().info('local_path:%s, hdfs_path:%s'%(local_path, hdfs_path))
    if not delete(hdfs_path):
        return False
    try:
        client.copy_from_local(local_path, hdfs_path)
        return True
    except Exception as e:
        if retry_time == -1:
            return False
        error_msg = traceback.format_exc()
        logger().error('uplaod faill error:%s'%(error_msg))
        return upload(local_path, hdfs_path, retry_time - 1)

@error(False)
def upload_dir(local_path, hdfs_path):
    if not os.path.exists(local_path):
        logger().error('local_path:%s not exists'%(local_path))
        return False
    if hdfs_path[-1] == os.sep:
        hdfs_path = hdfs_path[:-1]
    if local_path[-1] == os.sep:
        local_path = local_path[:-1]
    target_dir = local_path.split(os.sep)[-1]
    dir_tree = os.walk(local_path)
    for root, dirs, files in dir_tree:
        for file in files:
            path_element = root.split(os.sep)
            append_path = target_dir
            if path_element[-1] != target_dir:
                index = path_element.index(target_dir)
                append_path = os.sep.join(path_element[index:])
            hdfs_path_tmp = hdfs_path +os.sep + append_path
            if not client.exists(hdfs_path_tmp):
                client.mkdirs(hdfs_path_tmp)
            local_file_path = root + os.sep + file
            res = upload(local_file_path, hdfs_path_tmp)
            if not res:
                delete(local_path)
                return False
    return True

@error(None)
def get_job_id(job_name):
    def filter_app(x):
        target_name = x['name']
        return target_name == job_name
    apps_url = config.GET_CONF('hadoop', 'yarn_apps_url')
    if job_name.split('-')[-1] == 'class':
        apps_url = config.GET_CONF('hadoop', 'yarn_apps_url2')
    response = urllib2.urlopen(apps_url)
    data = response.read()
    data = json.loads(data)
    if not data['apps']:
        return None
    apps = data['apps']['app']
    target_apps = filter(filter_app, apps)
    if not target_apps:
        return None
    target_apps = sorted(target_apps, key=lambda x:x['startedTime'], reverse=True)
    target_app = target_apps[0]
    job_id = 'job' + target_app['id'].split('application')[1]
    return job_id

@error(None)
def get_job_progress(job_name):
    def filter_app(x):
        target_name = x['name']
        return target_name == job_name
    apps_url = config.GET_CONF('hadoop', 'yarn_apps_url')
    if job_name.split('-')[-1] == 'class':
        apps_url = config.GET_CONF('hadoop', 'yarn_apps_url2')
    response = urllib2.urlopen(apps_url)
    data = response.read()
    data = json.loads(data)
    if not data['apps']:
        return 0
    apps = data['apps']['app']
    target_apps = filter(filter_app, apps)
    progress = 0
    if target_apps:
        target_apps = sorted(target_apps, key=lambda x:x['startedTime'], reverse=True)
        target_app = target_apps[0]
        progress = int(target_app['progress'])
    logger().info('mr_job_name: %s, mr_progress:%s' % (job_name, progress))
    return progress


if __name__ == '__main__':
    #print upload_dir('./base','/tmp')
    #print upload('./log.py','/tmp')
    #print delete('/tmp/t.txt')
    #client.copy_from_local('/tmp/t.txt', '/tmp/t.txt')
    print download('/user/hwl/par.jar','./')
    #print listdir('/production/version1/auto/input')
    #print download_dir('/tmp/output/protocol','./')
    #print mkdirs('/tmp/a/s/d')
    #print upload_dir_v2('./base','/tmp')
    #print download_dir_v2('/tmp/input','./')
    #create_file('/tmp/6688.txt','tom', False)
    #res =  append('/tmp/6688.txti', 'tom\n')
    #print res
    #print get_file_checksum('/user/hwl/input/test4')
    #print get_file_status('/user/hwl/input/test4')
    #print type(res)
    #print download('/user/hwl/input/track_test', './')
    #print get_content_sum('/production/service-storage/step2/streaming_output/201581884_1_kss-upload-mapreduce_null_214367501')['length']
    #print get_content_sum('/production/service-storage/step2/streaming_output/400106787_1_kss-upload-mapreduce_null_6758929')
    #print get_job_id('element_400051160_1-class')
    #print get_xattr('/user/hwl/input/test4', 'user.atime')
    #print set_xattr('/user/hwl/input/test4', 'user.addr', 'bj', 'REPLACE')
    #print download_dir('/user/hwl/copy_data_result','/home/hadoop/hwl/model/123')
    #print get_active_namenode()


