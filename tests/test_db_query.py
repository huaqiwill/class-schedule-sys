import unittest
from common.utils import DBQuery


class TestDBUtils(unittest.TestCase):
    def test_exec(self):
        result = DBQuery("create table if not exists admin(username text, password text)").exec()
        print(result)
        result = DBQuery("insert into admin(username,password) values ('admin','admin')").exec()
        print(result)

    def test_query(self):
        result = DBQuery("select * from admin").dict()
        print(result)
        result = DBQuery("select * from admin").dict_list()
        print(result)
