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
            "create table if not exists teacher(id integer primary key autoincrement, name text, phone text, password text,position text)"
        ).exec()

    @staticmethod
    def save(teacher: dict):
        if TeacherInfo.info(teacher.get("id")) is None:
            return DBQuery(
                "insert into teacher(name,phone,password,position) values(?,?,?,?)",
                teacher["name"],
                teacher["phone"],
                teacher["password"],
                teacher["position"]
            ).exec()
        else:
            return DBQuery(
                "update teacher set name=?,phone=?,password=?,position=? where id=?",
                teacher["name"],
                teacher["phone"],
                teacher["password"],
                teacher["position"],
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
    def create_table(table: str):
        DBQuery(
            f"create table if not exists {table} (id integer primary key autoincrement ,WEEKDAY1 text,WEEKDAY2 text,WEEKDAY3 text,WEEKDAY4 text,WEEKDAY5 text)"
        ).exec()

    @staticmethod
    def save(table: str, course: dict):
        if CourseInfo.info(table, course.get("id")) is None:
            return DBQuery(
                f"insert into {table}(WEEKDAY1,WEEKDAY2,WEEKDAY3,WEEKDAY4,WEEKDAY5) values (?,?,?,?,?)",
                course["WEEKDAY1"],
                course["WEEKDAY2"],
                course["WEEKDAY3"],
                course["WEEKDAY4"],
                course["WEEKDAY5"]
            ).exec()
        else:
            return DBQuery(
                f"update {table} set WEEKDAY1=?, WEEKDAY2=?, WEEKDAY3=?, WEEKDAY4=?, WEEKDAY5=? where id=?",
                course["WEEKDAY1"],
                course["WEEKDAY2"],
                course["WEEKDAY3"],
                course["WEEKDAY4"],
                course["WEEKDAY5"],
                course["id"],
            ).exec()

    @staticmethod
    def delete(table: str, id: int):
        return DBQuery(f"delete from {table} where id=?", id).exec()

    @staticmethod
    def info(table: str, id: int):
        if id is None:
            return None
        return DBQuery(f"select * from {table} where id=?", id).dict()

    @staticmethod
    def list(table: str, page=1, limit=10):
        return DBQuery(f"select * from {table} limit ?,?", page, limit).dict_list()

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
            "create table if not exists student(id integer primary key autoincrement, name text, grade text, major text, class_num text,password text)"
        ).exec()

    @staticmethod
    def save(stu: dict):
        if StudentInfo.info(stu.get("id")) is None:
            return DBQuery(
                "insert into student( name, grade, major, class_num,password) values(?,?,?,?,?)",
                stu["name"],
                stu["grade"],
                stu["major"],
                stu["class_num"],
                stu["password"]
            ).exec()
        else:
            return DBQuery(
                "update student set name = ?, grade = ?, major = ?, class_num = ?,password=? where id = ?",
                stu["name"],
                stu["grade"],
                stu["major"],
                stu["class_num"],
                stu["password"],
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


class ClassesInfo(object):
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
    def save(table: str, cls: dict):
        if ClassesInfo.info(cls.get("id")) is None:
            return DBQuery(
                f"insert into {table}(WEEKDAY1, WEEKDAY2, WEEKDAY3, WEEKDAY4,WEEKDAY5) values (?,?,?,?,?)",
                cls["WEEKDAY1"],
                cls["WEEKDAY2"],
                cls["WEEKDAY3"],
                cls["WEEKDAY4"],
                cls["WEEKDAY5"],
            ).exec()
        else:
            return DBQuery(
                f"update {table} set WEEKDAY1 = ?, WEEKDAY2 = ?, WEEKDAY3 = ?, WEEKDAY4 = ?,WEEKDAY5=? where id = ?",
                cls["WEEKDAY1"],
                cls["WEEKDAY2"],
                cls["WEEKDAY3"],
                cls["WEEKDAY4"],
                cls["WEEKDAY5"],
                cls["id"],
            ).exec()

    @staticmethod
    def delete(id):
        return DBQuery("delete from classes where id = ?", id).exec()

    @staticmethod
    def info(id):
        if id is None:
            return None
        return DBQuery("select * from classes where id = ?", id).dict()

    @staticmethod
    def list(page=1, limit=10):
        return DBQuery("select * from classes limit ?,?", page, limit).dict_list()
