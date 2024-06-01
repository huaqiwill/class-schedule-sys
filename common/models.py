from common.utils import DBQuery, DBUtils2


class AdminInfo(object):
    """管理员信息
    username
    password
    """

    @staticmethod
    def create_table():
        DBQuery("create table if not exists admin(username text, password text)").exec()
        AdminInfo.init_super()

    @staticmethod
    def init_super():
        result = DBQuery("select * from admin where username = 'admin'").dict()
        if result is None:
            DBQuery("insert into admin(username, password) values('admin', 'admin')").exec()

    @staticmethod
    def login(username: str, password: str):
        """判断管理员是否登录成功"""
        return DBQuery("select * from admin where username = ? and password = ?", username, password).dict()

    @staticmethod
    def update_password(username: str, password: str):
        """更新管理员密码"""
        return DBQuery(
            "update admin set password=? where username=?",
            password,
            username,
        ).exec()


class TeacherInfo(object):
    """老师信息
    id
    name
    phone
    password
    """

    @staticmethod
    def create_table():
        return DBQuery(
            "create table if not exists teacher(id integer primary key autoincrement, name text, phone text, password text)"
        ).exec()

    @staticmethod
    def save(teacher: dict):
        if TeacherInfo.info(teacher.get("id")) is None:
            return DBQuery(
                "insert into teacher(name,phone,password) values(?,?,?)",
                teacher["name"],
                teacher["phone"],
                teacher["password"],
            ).exec()
        else:
            return DBQuery(
                "update teacher set name=?,phone=?,password=? where id=?",
                teacher["name"],
                teacher["phone"],
                teacher["password"],
                teacher["id"],
            ).exec()

    @staticmethod
    def delete(id: int):
        return DBQuery("delete from teacher where id=?", id).exec()

    @staticmethod
    def login(name: str, password: str):
        return DBQuery(
            "select * from teacher where name = ? and password = ?",
            name,
            password,
        ).dict()

    @staticmethod
    def info(id: int):
        if id is None:
            return None
        return DBQuery("select * from teacher where id=?", id).dict()

    @staticmethod
    def list(page=1, limit=10):
        return DBQuery("select * from teacher limit ?,?", page, limit).dict_list()


class CourseInfo(object):
    """课程信息
    id 课程ID
    name 课程的名称
    class_num 课程对应的班级编号
    credits 课程的学分
    schedule 课程的上课时间和地点
    """

    @staticmethod
    def create_table():
        return DBQuery(
            "create table if not exists course(id integer primary key autoincrement, name text, teacher text, class_num text, credits text, schedule text)"
        ).exec()

    @staticmethod
    def save(course: dict):
        if CourseInfo.info(course.get("id")) is None:
            return DBQuery(
                "insert into course(name,teacher,class_num,credits,schedule) values (?,?,?,?,?)",
                course["name"],
                course["teacher"],
                course["class_num"],
                course["credits"],
                course["schedule"],
            ).exec()
        else:
            return DBQuery(
                "update course set name=?, teacher=?, class_num=?, credits=?, schedule=? where id=?",
                course["name"],
                course["teacher"],
                course["class_num"],
                course["credits"],
                course["schedule"],
                course["id"],
            ).exec()

    @staticmethod
    def delete(id: int):
        return DBQuery("delete from course where id=?", id).exec()

    @staticmethod
    def info(id: int):
        if id is None:
            return None
        return DBQuery("select * from course where id=?", id).dict()

    @staticmethod
    def list(page=1, limit=10):
        return DBQuery("select * from course limit ?,?", page, limit).dict_list()

    @staticmethod
    def course_page(page=1, limit=10):
        return DBQuery("SELECT * FROM C1G9 limit ?,?", page, limit).dict_list()

    @staticmethod
    def table_fields():
        return DBUtils2().get_table_fields("C1G9")


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
        return DBQuery(
            "create table if not exists student(id integer primary key autoincrement, name text, grade text, major text, class_num text)"
        ).exec()

    @staticmethod
    def save(stu: dict):
        if StudentInfo.info(stu.get("id")) is None:
            return DBQuery(
                "insert into student( name, grade, major, class_num) values(?,?,?,?)",
                stu["name"],
                stu["grade"],
                stu["major"],
                stu["class_name"],
            ).exec()
        else:
            return DBQuery(
                "update student set name = ?, grade = ?, major = ?, class_num = ? where id = ?",
                stu["name"],
                stu["grade"],
                stu["major"],
                stu["class_name"],
                stu["id"],
            ).exec()

    @staticmethod
    def delete(id: int):
        return DBQuery("delete from student where id = ?", id).exec()

    @staticmethod
    def info(id: int):
        if id is None:
            return None
        return DBQuery("select * from student where id = ?", id).dict()

    @staticmethod
    def list(page=1, limit=10):
        return DBQuery("select * from student limit ?,?", page, limit).dict_list()

    @classmethod
    def fields_names(cls):
        return DBUtils2().get_table_fields("student")


class ClassInfo(object):
    """班级信息
    id
    name
    level
    teacher
    time
    """

    @staticmethod
    def create_table():
        return DBQuery(
            "create table if not exists classes(id integer primary key autoincrement, name text, teacher text, time text, place text)"
        ).exec()

    @staticmethod
    def save(cls: dict):
        if ClassInfo.info(cls["id"]) is None:
            return DBQuery(
                "update classes set name = ?, teacher = ?, time = ?, place = ? where id = ?",
                cls["id"],
                cls["name"],
                cls["teacher"],
                cls["time"],
                cls["place"],
            ).exec()
        else:
            return DBQuery(
                "update classes set name = ?, teacher = ?, time = ?, place = ? where id = ?",
                cls["id"],
                cls["name"],
                cls["teacher"],
                cls["time"],
                cls["place"],
            ).exec()

    @staticmethod
    def delete(id):
        return DBQuery("delete from classes where id = ?", id).exec()

    @staticmethod
    def info(id):
        return DBQuery("select * from classes where id = ?", id).dict()

    @staticmethod
    def list(page=1, limit=10):
        return DBQuery("select * from classes limit ?,?", page, limit).dict_list()
