import json

from PySide6.QtSql import QSqlDatabase, QSqlQuery
import os
import logging
import sqlite3
import csv
from common import config

def dict_list_to_csv(data, filename):
    fieldnames = data[0].keys()
    with open(filename, 'w', newline='', encoding="utf8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # 写入列名
        writer.writeheader()
        # 写入数据行
        writer.writerows(data)


def csv_to_dict_list(filename) -> list[dict]:
    with open(filename, 'r', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        # 将读取的行转换为字典并存储在列表中
        data = [row for row in reader]
        return data


class DBQuery(object):
    def __init__(self, sql: str, *args):
        self.db = DBUtils2()
        self.sql = sql
        self.args = args

    def last_error(self):
        return self.db.get_error_msg()

    def last_sql(self):
        return self.sql.replace("?", "{}").format(*self.args)

    def exec(self):
        result = self.db.exec(self.sql, list(self.args))
        if not result:
            logging.error("sql执行 [{0}] 失败, 原因 {1}".format(self.last_sql(), self.last_error()))
        return result

    def dict(self):
        result = self.db.query(self.sql, list(self.args)).get_dict()
        if not result:
            logging.error("sql执行 [{0}] 失败, 原因 {1}".format(self.last_sql(), self.last_error()))
            return None
        return result

    def dict_list(self):
        args = list(self.args)
        args[0] = args[0] - 1
        result = self.db.query(self.sql, args).get_dict_list()
        if not result:
            logging.error("sql 执行 [{0}] 失败, 原因 {1}".format(self.last_sql(), self.last_error()))
            return []
        return result


class DBUtils(object):
    db_name = os.path.join(os.getcwd(), "data\\ClassSchedules.db")
    _db_utils = None

    def __init__(self) -> None:
        self.connect()
        self.__query_status = False

    def connect(self):
        if not QSqlDatabase.contains("qt_sql_default_connection"):
            self.__db = QSqlDatabase.addDatabase("QSQLITE", "qt_sql_default_connection")
            self.__db.setDatabaseName(self.db_name)
            if not self.__db.open():
                logging.error("数据库打开失败")
                raise Exception("数据库打开失败")
        else:
            self.__db = QSqlDatabase.database("qt_sql_default_connection")
        if self.__db.isOpen():
            logging.info("数据库连接成功")
        else:
            logging.error("数据库连接失败")

    def error(self):
        return self.__query_instance.lastError().text()

    def close(self):
        if not self.__db:
            self.__db.close()

    def __check(self):
        if self.__query_instance is None:
            raise Exception("query_instance is None")
        if self.__query_status is None:
            logging.error("__query_status is False")

    def query(self, sql: str, *args):
        self.__query_instance = QSqlQuery()
        self.__query_instance.prepare(sql)
        for arg in args:
            self.__query_instance.addBindValue(arg)
        self.__query_instance.exec()
        return self

    def exec(self, sql: str, *args):
        self.query(sql, args)
        return self.__query_status

    def dict_list(self):
        self.__check()
        # 获取查询结果的列名
        field_names = [
            self.__query_instance.record().fieldName(i)
            for i in range(self.__query_instance.record().count())
        ]
        # 将查询结果转换为字典列表
        result_list = []
        while self.__query_instance.next():
            record = {
                field_names[i]: self.__query_instance.value(i)
                for i in range(len(field_names))
            }
            result_list.append(record)

        return result_list, field_names

    def dict(self):
        self.__check()
        field_names = [
            self.__query_instance.record().fieldName(i)
            for i in range(self.__query_instance.record().count())
        ]
        while self.__query_instance.next():
            record = {
                field_names[i]: self.__query_instance.value(i)
                for i in range(len(field_names))
            }
            return record, field_names
        return None


class DBUtils2(object):
    def __init__(self):
        self.db_file = config.db_file
        # self.db_file = os.path.join(os.getcwd(), "data\\ClassSchedules.db")
        # self.db_file = r"D:\Peng\ABC\商单列表\2024\2024.05\2024.5.30_300\class-schedule-sys\data\test.db"
        self.connection = sqlite3.connect(self.db_file)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.error_msg = None

    def close(self):
        self.cursor.close()
        self.connection.close()

    def exec(self, sql: str, args=[]):
        try:
            self.cursor.execute(sql, args)
            self.connection.commit()
            return True
        except Exception as e:
            self.error_msg = e
            return False

    def query(self, sql: str, args=[]):
        try:
            self.cursor.execute(sql, args)
        except Exception as e:
            self.error_msg = e
        return self

    def get_error_msg(self):
        return self.error_msg

    def get_table_fields(self, table_name):
        """ 获取表的字段名 """
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            rows = self.cursor.fetchall()
            fields = [row[1] for row in rows]
            return fields
        except Exception as e:
            self.error_msg = e
            return []

    def get_dict(self):
        if self.error_msg:
            return None

        row = self.cursor.fetchone()
        if row:
            return dict(row)
        return None

    def get_dict_list(self):
        if self.error_msg:
            return None
        rows = self.cursor.fetchall()
        result = []
        for row in rows:
            result.append(dict(row))
        return result
