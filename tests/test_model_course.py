from common.models import CourseInfo
import unittest


class TestCourse(unittest.TestCase):
    def test_create(self):
        result = CourseInfo.create_table()
        print(result)

    def test_save(self):
        result = CourseInfo.save({
            "name": "张三",
            "teacher": "123456",
            "class_num": "12552",
            "credits": "123456",
            "schedule": "123456",
        })
        print(result)

    def test_delete(self):
        result = CourseInfo.delete(1)
        print(result)

    def test_info(self):
        result = CourseInfo.info(2)
        print(result)

    def test_list(self):
        result = CourseInfo.list()
        print(result)


if __name__ == "__main__":
    unittest.main()
