#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
from optparse import OptionParser
from singleton import *
import os
import time
import sys

optParser = OptionParser()
optParser.add_option("-p", "--project", type="string", dest="project", help='')
optParser.add_option("-e", "--env", type="string", dest="env", help='')

env = 'dev' 

try:
    import jaguar_v1
    ENV_PROJ_HOME = jaguar_v1.ENV_PROJ_HOME
    conf_file = '%s/conf/service_conf_%s.ini' % (ENV_PROJ_HOME, env)
except:
    env = os.getenv('env')
    conf_file = './service_conf_%s.ini' % env
    sys.stderr.write('now conf file is [%s]\n' % conf_file)


@singleton
class __ServiceManager():
    def __init__(self):
        self.conf_file = conf_file 
        self.load()

    def load(self):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.conf_file)
        self.mtime = os.path.getmtime(self.conf_file)
        sys.stderr.write('load conf file at [%s]\n' % time.ctime(time.time()))

    def reload(self):
        if self.mtime != os.path.getmtime(self.conf_file):
            self.load()

    def get_ex(self, name, key, dft_val):
        self.reload()
        try:
            return self.cf.get(name, key)
        except Exception, e:
            print e
            return dft_val

    def get(self, name, key):
        self.reload()
        return self.cf.get(name, key)

    def has(self, name, key):
        return self.cf.has_option(name, key)


def GET_CONF_EX(name, key, dft_val):
    manager = __ServiceManager()
    return manager.get_ex(name, key, dft_val)


def GET_CONF(name, key):
    manager = __ServiceManager()
    return manager.get(name, key)


def HAS_CONF(name, key):
    manager = __ServiceManager()
    return manager.has(name, key)


def SET_CONF_ENV(project_name, config_env):
    global conf_file
    try:
        if ENV_PROJ_HOME:
            conf_file = os.path.join(ENV_PROJ_HOME,
                    'conf/service_conf_' + config_env + '.ini')
        else:
            conf_file = './service_conf_%s.ini' % config_env
                              
    except:
        conf_file = './service_conf_%s.ini' % config_env


    manager = __ServiceManager()
    manager.project_name = project_name
    manager.config_env = config_env
    manager.conf_file = conf_file 
    manager.mtime = os.path.getmtime(manager.conf_file)
    manager.load()


def main():
    print GET_CONF('hadoop', 'hdfs_root_dir')
    print GET_CONF('sentinel', 'hosts')


if __name__ == '__main__':
    main()
