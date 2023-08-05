# -*- coding:utf-8 -*-
from SCLibrary.builtin.util import get_robot_variable_value
from SCLibrary.base import keyword
from robot.libraries.BuiltIn import BuiltIn


class Env(object):
    def __init__(self):
        self.env = get_robot_variable_value("${RF_REAL_ENV}", "dev")

    @keyword("If Dev")
    def if_dev(self, name, *args):
        # *args:元组
        return BuiltIn().run_keyword_if(self.env == "dev", name, *args)

    @keyword("If Prepub")
    def if_prepub(self, name, *args):
        return BuiltIn().run_keyword_if(self.env == "prepub", name, *args)

    @keyword("If Prod")
    def if_prod(self, name, *args):
        return BuiltIn().run_keyword_if(self.env == "prod", name, *args)

