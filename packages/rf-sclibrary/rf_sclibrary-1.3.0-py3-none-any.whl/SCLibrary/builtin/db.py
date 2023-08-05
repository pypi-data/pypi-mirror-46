# -*- coding:utf-8 -*-

from DatabaseLibrary.connection_manager import ConnectionManager
from DatabaseLibrary.query import Query
from DatabaseLibrary.assertion import Assertion
from SCLibrary.base import keyword
import json

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from .websql import WebSQL


class DBKeywords(ConnectionManager, Query, Assertion):
    env = 'dev'
    websql = None
    host = ''
    db = ''

    def __init__(self):
        super().__init__()
        built_in = BuiltIn()
        self.env = built_in.get_variable_value("${RF_ENV}", 'dev')
        if self.env == 'prepub' or self.env == 'prod':
            uname = built_in.get_variable_value("${WEBSQL_UNAME}", '')
            pwd = built_in.get_variable_value("${WEBSQL_PWD}", '')
            if uname == '' or pwd == '':
                logger.error('线上环境需要填写WebSQL用户密码: WEBSQL_UNAME, WEBSQL_PWD')
                return
            self.websql = WebSQL(uname, pwd)

    @keyword("DB Connect")
    def db_connect_to_mysql(self, db):
        """ 连接数据库
        ``db`` 字典，例：{'db':'mysql','host':'172.17.40.214','port=7003','name=todo','user':'root','pwd':'root'}
        其中db为连接的数据库类型名称，默认mysql,  name为数据库名
        """
        if self.env == 'prepub' or self.env == 'prod':
            self.host = db['host']
            self.db = db['db']
            return

        module = db['db'] if 'db' in db else 'pymysql'
        if module.upper() == 'MYSQL':
            module = 'pymysql'
        elif module.upper() == 'POSTGRESQL' or module.upper() == 'PGSQL':
            module = 'psycopg2'
        super(DBKeywords, self).connect_to_database(dbapiModuleName=module, dbName=db['name'],
                                                    dbUsername=db['user'], dbPassword=db['pwd'], dbHost=db['host'], dbPort=db['port'], dbCharset='utf8')

    @keyword("DB Disconnect From Database")
    def db_disconnect_db(self):
        """ 断开所有的数据库连接 """
        if self.env == 'prepub' or self.env == 'prod':
            return
        super(DBKeywords, self).disconnect_from_database()

    @keyword("DB Query")
    def db_query(self, selectStatement, sansTran=False, returnAsDict=True):
        """ 连接数据库
        ``selectStatement``  select语句

        ``sansTran`` 是否处于事务

        ``returnAsDict`` 结果作为字典返回，默认True
        """
        if self.env == 'prepub' or self.env == 'prod':
            return self.websql.query(self.host, self.db, selectStatement)
        return super(DBKeywords, self).query(selectStatement, sansTran, returnAsDict)

    @keyword("DB Execute Sql Script")
    def db_execute_sql_script(self, sqlScriptFileName, sansTran=False):
        """ 执行一个SQL脚本文件
        ``sqlScriptFileName``  脚本目录

        ``sansTran`` 是否处于事务
        """
        if self.env == 'prepub' or self.env == 'prod':
            return self.websql.query(self.host, self.db, sqlScriptFileName)
        return super(DBKeywords, self).execute_sql_script(sqlScriptFileName, sansTran)

    @keyword("DB Execute Sql String")
    def db_execute_sql_string(self, sqlString, sansTran=False):
        """ 执行一个SQL
        ``sqlString``  sql

        ``sansTran`` 是否处于事务
        """
        if sqlString.startswith('select') or sqlString.startswith('SELECT'):
            if self.env == 'prepub' or self.env == 'prod':
                return self.websql.query(self.host, self.db, sqlString)
            return self.query(sqlString, sansTran, True)

        if self.env == 'prepub' or self.env == 'prod':
            logger.error('预发／线上环境禁止非读操作!')
            return None
        return super(DBKeywords, self).execute_sql_string(
            sqlString, sansTran)

    @keyword("DB Execute")
    def de_execute(self, sqlString, sansTran=False):
        """ 执行一个SQL
        ``sqlString``  sql

        ``sansTran`` 是否处于事务
        """
        self.db_execute_sql_string(sqlString, sansTran=False)

    @keyword("DB Check If Exists In Database")
    def db_exists_in_db(self, selectStatement, sansTran=False):
        """ 断言查询结果是否存在
        ``selectStatement``  查询语句

        ``sansTran`` 是否处于事务
        """
        if self.env == 'prepub' or self.env == 'prod':
            result = self.db_query(selectStatement)
            if len(result) <= 0:
                raise AssertionError("Expected to have have at least one row from '%s' "
                                 "but got 0 rows." % selectStatement)
            return
        super(DBKeywords, self).check_if_exists_in_database(
            selectStatement, sansTran)

    @keyword("DB Check If Not Exists In Database")
    def db_not_exists_in_db(self, selectStatement, sansTran=False):
        """ 断言查询结果是否不存在 """
        if self.env == 'prepub' or self.env == 'prod':
            result = self.db_query(selectStatement)
            if len(result) > 0:
                raise AssertionError("Expected to have have no rows from '%s' "
                                 "but got some rows : %s." % (selectStatement, result))
            return
        super(DBKeywords, self).check_if_not_exists_in_database(
            selectStatement, sansTran)
