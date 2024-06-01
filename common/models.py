from PySide6.QtSql import QSqlQuery
from common.utils import DBUtils


class AdminInfo(object):
    """
    管理员信息
    ：管理员可以创建课程、老师、班级、学习
    """

    @staticmethod
    def create_table():
        res = DBUtils().exec(
            "create table if not exists admin(username text, password text)"
        )
        AdminInfo.init_super()
        return res

    @staticmethod
    def init_super():
        if (
                DBUtils().query("select * from admin where username = 'admin'").dict()
                is None
        ):
            DBUtils().exec(
                "insert into admin(username, password) values('admin', 'admin')"
            )

    @staticmethod
    def login(username: str, password: str):
        """判断管理员是否登录成功"""
        return (
            DBUtils()
                .query(
                "select * from admin where username = ? and password = ?",
                username,
                password,
            )
                .dict()
        )

    @staticmethod
    def update_password(username: str, password: str):
        """更新管理员密码"""
        return DBUtils().exec(
            "update admin set password=? where username=?",
            password,
            username,
        )


class TeacherInfo(object):
    """老师信息
    老师可以创建学生、课程
    """

    @staticmethod
    def create_table():
        return DBUtils().exec(
            "create table if not exists teacher(id integer primary key autoincrement, name text, phone text, password text)"
        )

    @staticmethod
    def save(teacher: dict):
        print(TeacherInfo.info(teacher.get("id")))
        if TeacherInfo.info(teacher.get("id")) is None:
            return DBUtils().exec(
                "insert into teacher(name,phone,password) values(?,?,?)",
                teacher["name"],
                teacher["phone"],
                teacher["password"],
            )
        else:
            return DBUtils().exec(
                "update teacher set name=?,phone=?,password=? where id=?",
                teacher["name"],
                teacher["phone"],
                teacher["password"],
                teacher["id"],
            )

    @staticmethod
    def delete(id: int):
        DBUtils().exec("delete from teacher where id=?", id)

    @staticmethod
    def login(name: str, password: str):
        return DBUtils().query(
            "select * from teacher where name = ? and password = ?",
            name,
            password,
        ).dict()


@staticmethod
def info(id: int):
    if id is None:
        return None
    return DBUtils().query("select * from teacher where id=?", id).dict()


@staticmethod
def list(page=1, limit=10):
    return (
        DBUtils().query("select * from teacher limit ?,?", page, limit).dict_list()
    )


class CourseInfo(object):
    """
    课程编号（Course ID）: 唯一标识一门课程。
    课程名称（Course Name）: 课程的名称，如“数学”或“英语”。
    教师（Teacher）: 授课教师的名字或教师编号。
    班级编号（Class ID）: 课程对应的班级编号。
    学分（Credits）: 课程的学分（如果适用）。
    课程时间（Schedule）: 课程的上课时间和地点
    """

    @staticmethod
    def create_table():
        return DBUtils().exec(
            "create table if not exists course_info(id integer primary key autoincrement, name text, teacher text, class_num text, credits text, schedule text)"
        )

    @staticmethod
    def save(course: dict):
        if CourseInfo.info(course) is None:
            return DBUtils().exec(
                "update course_info set name=?, teacher=?, class_num=?, credits=?, schedule=? where id=?",
                course["name"],
                course["teacher"],
                course["class_num"],
                course["credits"],
                course["schedule"],
                course["id"],
            )
        else:
            return DBUtils().exec(
                "update course_info set name=?, teacher=?, class_num=?, credits=?, schedule=? where id=?",
                course["name"],
                course["teacher"],
                course["class_num"],
                course["credits"],
                course["schedule"],
                course["id"],
            )

    @staticmethod
    def delete(self):
        return DBUtils().exec("delete from course_info where id=?", self.id)

    @staticmethod
    def info(id):
        return DBUtils().query("select * from course_info", id).dict()

    @staticmethod
    def list(id):
        return DBUtils().query("select * from course_info").dict_list()


class StudentInfo(object):
    """
    学生信息表
    id: 学生ID
    name: 学生姓名
    grade: 年级
    major: 专业
    class_num: 班级
    """

    @staticmethod
    def create_table():
        return DBUtils().exec(
            "create table if not exists student(id integer primary key autoincrement, name text, grade text, major text, class_num text)"
        )

    @staticmethod
    def save(stu: dict):
        if StudentInfo.info(stu.get("id")) is None:
            return DBUtils().exec(
                "insert into student( name, grade, major, class_num) values(?,?,?,?)",
                stu["name"],
                stu["grade"],
                stu["major"],
                stu["class_name"],
            )
        else:
            return DBUtils().exec(
                "update student set name = ?, grade = ?, major = ?, class_num = ? where id = ?",
                stu["name"],
                stu["grade"],
                stu["major"],
                stu["class_name"],
                stu["id"],
            )

    @staticmethod
    def delete(id: int):
        return DBUtils().exec("delete from student where id = ?", id)

    @staticmethod
    def info(id: int):
        if id is None:
            return None
        return DBUtils().query("select * from student where id = ?", id).dict()

    @staticmethod
    def list(page=1, limit=10):
        return (
            DBUtils().query("select * from student limit ?,?", page, limit).dict_list()
        )

    @staticmethod
    def fields():
        return DBUtils().query("select * from student limit 1").fields()


class ClassInfo(object):
    """班级信息
    self.id = id
    self.name = name
    self.level = level
    self.teacher = teacher
    self.time = time
    self.trem = place
    """

    @staticmethod
    def create_table():
        return DBUtils().exec(
            "create table if not exists classes(id integer primary key autoincrement, name text, teacher text, time text, place text)"
        )

    @staticmethod
    def save(cls: dict):
        if ClassInfo.info(cls["id"]) is None:
            return DBUtils().exec(
                "update classes set name = ?, teacher = ?, time = ?, place = ? where id = ?",
                cls["id"],
                cls["name"],
                cls["teacher"],
                cls["time"],
                cls["place"],
            )
        else:
            return DBUtils().exec(
                "update classes set name = ?, teacher = ?, time = ?, place = ? where id = ?",
                cls["id"],
                cls["name"],
                cls["teacher"],
                cls["time"],
                cls["place"],
            )

    @staticmethod
    def delete(self, id):
        return DBUtils().exec("delete from classes where id = ?", id)

    @staticmethod
    def info(id):
        return DBUtils().query("select * from classes where id = ?", id).dict()

    @staticmethod
    def list(page=1, limit=10):
        return (
            DBUtils()
                .query("select * from classes limit ?,?", page, limit)
                .dict_list()
        )
