import unittest
from common.utils import DBUtils2


class TestDBUtils(unittest.TestCase):
    def test_exec(self):
        db = DBUtils2()
        result = db.exec("create table if not exists admin(username text, password text)")
        if not result:
            print(db.get_error_msg())
        print(result)
        result = db.exec("insert into admin(username,password) values ('admin','admin')")
        print(result)
        db.close()

    def test_query(self):
        db = DBUtils2()
        result = db.query("select * from admin").get_dict()
        print(result)
        result = db.query("select * from admin").get_dict_list()
        print(result)
        db.close()
