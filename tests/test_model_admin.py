from common.models import AdminInfo
import unittest


class TestStudent(unittest.TestCase):
    def test_create(self):
        result = AdminInfo.create_table()
        print(result)

    def test_update_password(self):
        result = AdminInfo.update_password("admin", "admin1")
        print(result)
        result = AdminInfo.update_password("admin", "admin")
        print(result)

    def test_login(self):
        result = AdminInfo.login("admin", "admin")
        print(result)


if __name__ == "__main__":
    unittest.main()
