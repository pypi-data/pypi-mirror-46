# -*- coding:utf-8 -*-
import logging
import time
import sys
initialized = False
formatter = logging.Formatter(
    ('%(asctime)s %(levelname)s %(process)d'
    '[%(filename)s:%(lineno)d %(funcName)s]: %(message)s'))

class Configer(object):
    def __init__(self):
        self.__log_path = ""
        self.__file_handler = None
        self.__console_handler = None
        self.__pure_path = ""
        self.__time_format = "%Y%m%d%H%M"
        self.__time_format = "%Y%m%d"

    inst = None

    @staticmethod
    def get():
        if Configer.inst is None:
            Configer.inst = Configer()
        return Configer.inst

    def set_file_handler(self):
        date_str = time.strftime(self.__time_format)
        self.__log_path = self.__pure_path + '.' + date_str

        fh = logging.FileHandler(self.__log_path)
        fh.setFormatter(formatter)
        self.__file_handler = fh
        logging.getLogger('').addHandler(fh)

    def set_console_handler(self):
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        self.__console_handler = console
        logging.getLogger('').addHandler(console)
        logging.getLogger('').setLevel(logging.INFO)

    def del_console_handler(self):
        logging.getLogger('').removeHandler(self.__console_handler)
        del self.__console_handler
        self.__console_handler = None

    def del_file_handler(self):
        logging.getLogger('').removeHandler(self.__file_handler)
        del self.__file_handler
        self.__file_handler = None

    def rotate(self):
        date_str = time.strftime(self.__time_format)
        path = self.__pure_path + '.' + date_str

        #sys.stderr.write('path:%s, old_path:%s\n' % (path, self.__log_path))
        #sys.stderr.flush()
        if path == self.__log_path:
            return
        sys.stdout.flush()
        sys.stderr.flush()
        self.del_file_handler()
        self.set_file_handler()

    def init(self, level, path="./log.txt", quiet=False):
        self.__pure_path = path
        if quiet:
            self.del_console_handler()
        if not quiet and not self.__console_handler:
            self.set_console_handler()
        self.set_file_handler()

        cmd = "logging.getLogger("").setLevel(logging.%s)" % (level.upper())
        exec cmd


class Logger(object):
    def __init__(self):
        self.info = logging.info
        self.debug = logging.debug
        self.warning = logging.warning
        self.error = logging.error
        self.critical = logging.critical
        Configer.get().set_console_handler()


def log_init(level, path="./log.txt", quiet=False):
    global initialized # pylint: disable=W0603
    if initialized:
        return
    Configer.get().init(level, path, quiet)
    initialized = True

g_logger = Logger()
def logger():
    Configer.get().rotate()
    return g_logger

if __name__ == '__main__':
    log_init('info', './log.txt', quiet=False) 
    while True:
        l = logger()
        l.info('abc')
        time.sleep(1)




