from common.models import StudentInfo
import unittest


class TestStudent(unittest.TestCase):
    def test_create(self):
        result = StudentInfo.create_table()
        print(result)

    def test_save(self):
        result = StudentInfo.save({
            "grade": "张三",
            "name": "123456",
            "major": "12552",
            "class_name": "123456",
        })
        print(result)

    def test_delete(self):
        result = StudentInfo.delete(2)
        print(result)

    def test_info(self):
        result = StudentInfo.info(2)
        print(result)

    def test_list(self):
        result = StudentInfo.list()
        print(result)


if __name__ == "__main__":
    unittest.main()
