from PySide6.QtSql import QSqlQuery


class Student:
    def __init__(self, name, id, grade, major, class_num):
        self.id = id
        self.name = name
        self.grade = grade
        self.major = major
        self.class_num = class_num

    def stu_add(self, stu):
        query = QSqlQuery()
        query.prepare("insert into FROM C1G7 WHERE ROWID = :rowid")
        query.addBindValue(":rowid", "")
        return query.exec()

    def stu_del(self, id):
        query = QSqlQuery()
        query.prepare("delete from student where id = :id")
        query.addBindValue(":id", id)
        return query.exec()

    def stu_upd(self, stu):
        query = QSqlQuery()
        query.prepare(
            "update student set name = :name, grade = :grade, major = :major, class_num = :class_num where id = :id"
        )
        query.addBindValue(":name", stu.name)
        query.addBindValue(":grade", stu.grade)
        query.addBindValue(":major", stu.major)
        query.addBindValue(":class_num", stu.class_num)
        query.addBindValue(":id", stu.id)
        return query.exec()

    def stu_info(self, id):
        query = QSqlQuery()
        query.prepare("select * from student where id = :id")
        query.addBindValue(":id", id)
        if query.exec():
            query.next()
            return (query.value(1),)

    def stu_all(self):
        query = QSqlQuery()
        query.prepare("select * from student")
        if query.exec():
            while query.next():
                yield (
                    query.value(0),
                    query.value(1),
                    query.value(2),
                    query.value(3),
                    query.value(4),
                )


class Classes:
    def __init__(self, id, name, teacher, time, place):
        self.id = id
        self.name = name
        self.teacher = teacher
        self.time = time
        self.place = place

    def class_add(self, cls):
        query = QSqlQuery()
        query.prepare("insert into FROM C1G7 WHERE ROWID = :rowid")
        query.addBindValue(":rowid", "")
        return query.exec()
    
    def class_del(self, id):
        query = QSqlQuery()
        query.prepare("delete from classes where id = :id")
        query.addBindValue(":id", id)
        return query.exec()
    
    def class_upd(self, cls):
        query = QSqlQuery()
        query.prepare(
            "update classes set name = :name, teacher = :teacher, time = :time, place = :place where id = :id"
        )
        query.addBindValue(":name", cls.name)
        query.addBindValue(":teacher", cls.teacher)
        query.addBindValue(":time", cls.time)
        
        query.addBindValue(":place", cls.place)
        query.addBindValue(":id", cls.id)
        return query.exec()
    
    def class_info(self, id):
        query = QSqlQuery()
        query.prepare("select * from classes where id = :id")
        query.addBindValue(":id", id)
        if query.exec():
            query.next()
            return (query.value(1),)
        return None
    
    def class_all(self):
        query = QSqlQuery()
        query.prepare("select * from classes")
        if query.exec():
            while query.next():
                yield (
                    query.value(0),
                    query.value(1),
                    query.value(2),
                    query.value(3),
                    query.value(4),
                )