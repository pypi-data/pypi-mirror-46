# -*- coding:utf-8 -*-
import os, shutil
from gevent import monkey
monkey.patch_all()
from SCLibrary.base import DynamicCore, hook_zh
from robot.api import logger
from SCLibrary.builtin import SelectKeywords
from SCLibrary.builtin import RandomKeywords
from SCLibrary.builtin import LogListener
from SCLibrary.builtin import DBKeywords
from SCLibrary.builtin import RequesterKeywords
from SCLibrary.builtin import UtilKeywords, get_robot_variable_value
from SCLibrary.builtin import LocustKeyword
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from SCLibrary.base import DynamicCore, hook_zh
from SCLibrary.builtin import Env
__version__ = '1.3.1'


class SCLibrary(DynamicCore):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self):
        libraries = [UtilKeywords(), RequesterKeywords(),
                     DBKeywords(), RandomKeywords(), SelectKeywords(), LocustKeyword(), Env()]
        DynamicCore.__init__(self, libraries)
        if get_robot_variable_value("${RF_DEBUG}") == True:
            self.ROBOT_LIBRARY_LISTENER = LogListener()
        # 复写robot的unic.py，支持Log打印中文
        # hook_zh()
        self._remove_result()

    def _remove_result(self):
        try:
            result_path = '%s/result' % os.getcwd()
            shutil.rmtree(result_path)
        except Exception:
            pass
