import unittest
from common.models import TeacherInfo


class TestTeacher(unittest.TestCase):
    def test_create(self):
        result = TeacherInfo.create_table()
        print(result)

    def test_teacher_info(self):
        teacher = TeacherInfo.info(1)
        print(teacher)
        self.assertEqual(teacher['name'], '张三')
        self.assertEqual(teacher['password'], '123456')

    def test_teacher_login(self):
        teacher = TeacherInfo.login('张三', '123456')
        print(teacher)

    def test_teacher_save(self):
        teacher = {
            'name': '李四',
            'password': '123456',
            'sex': '男',
            'age': 18,
            'phone': '12345678901',
            'email': '12345678901@qq.com',
            'address': '北京',
            'remark': '备注'
        }
        teacher = TeacherInfo.save(teacher)
        print(teacher)
