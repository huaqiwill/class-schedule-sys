import sys
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
)
from qfluentwidgets import (
    FluentWindow,
    FluentIcon as FIF,
    MessageBox as Msg,
)
from class_schedule import (
    Class1Grade7Interface,
    Class2Grade7Interface,
    Class3Grade7Interface,
    Class1Grade8Interface,
    Class2Grade8Interface,
    Class3Grade8Interface,
    Class1Grade9Interface,
    Class2Grade9Interface,
    Class3Grade9Interface,
    StudentManage,
    ClassManage,
    TeacherManage,
)
from common.models import AdminInfo, StudentInfo, TeacherInfo, CourseInfo, ClassInfo


class MainWindow(FluentWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initWindow()

        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)
        self.setCustomBackgroundColor(QColor(240, 244, 249), QColor(32, 32, 32))

        self.class1_grade7_interface = Class1Grade7Interface(self)
        self.class1_grade7_interface.setObjectName("class1_grade7_interface")
        self.class2_grade7_interface = Class2Grade7Interface(self)
        self.class2_grade7_interface.setObjectName("class2_grade7_interface")
        self.class3_grade7_interface = Class3Grade7Interface(self)
        self.class3_grade7_interface.setObjectName("class3_grade7_interface")
        self.class1_grade8_interface = Class1Grade8Interface(self)
        self.class1_grade8_interface.setObjectName("class1_grade8_interface")
        self.class2_grade8_interface = Class2Grade8Interface(self)
        self.class2_grade8_interface.setObjectName("class2_grade8_interface")
        self.class3_grade8_interface = Class3Grade8Interface(self)
        self.class3_grade8_interface.setObjectName("class3_grade8_interface")
        self.class1_grade9_interface = Class1Grade9Interface(self)
        self.class1_grade9_interface.setObjectName("class1_grade9_interface")
        self.class2_grade9_interface = Class2Grade9Interface(self)
        self.class2_grade9_interface.setObjectName("class2_grade9_interface")
        self.class3_grade9_interface = Class3Grade9Interface(self)
        self.class3_grade9_interface.setObjectName("class3_grade9_interface")

        self.student_manage = StudentManage(self)
        self.student_manage.setObjectName("student_manage")
        self.class_manage = ClassManage(self)
        self.class_manage.setObjectName("class_manage")
        self.teacher_manage = TeacherManage(self)
        self.teacher_manage.setObjectName("teacher_manage")

        # add items to navigation interface
        self.initNavigation()
        self.initData()

    def initNavigation(self):
        # self.addSubInterface(self.class1_grade7_interface, FIF.BUS, "初一(1)班")
        # self.addSubInterface(self.class2_grade7_interface, FIF.CAR, "初一(2)班")
        # self.addSubInterface(self.class3_grade7_interface, FIF.EDUCATION, "初一(3)班")
        # self.addSubInterface(self.class1_grade8_interface, FIF.IOT, "初二(1)班")
        # self.addSubInterface(self.class2_grade8_interface, FIF.COPY, "初二(2)班")
        # self.addSubInterface(self.class3_grade8_interface, FIF.CALENDAR, "初二(3)班")
        # self.addSubInterface(self.class1_grade9_interface, FIF.CHAT, "初三(1)班")
        # self.addSubInterface(self.class2_grade9_interface, FIF.FLAG, "初三(2)班")
        # self.addSubInterface(self.class3_grade9_interface, FIF.PALETTE, "初三(3)班")
        self.addSubInterface(self.student_manage, FIF.BUS, "学生管理")
        self.addSubInterface(self.class_manage, FIF.BUS, "班级管理")
        self.addSubInterface(self.teacher_manage, FIF.BUS, "教师管理")

    def initWindow(self):
        self.resize(800, 600)
        self.setWindowTitle("学生课表系统")

    def initData(self):
        if not AdminInfo.create_table():
            Msg("错误", "管理员信息创建错误", self).show()
        if not StudentInfo.create_table():
            Msg("错误", "学生信息创建错误", self).show()
        if not TeacherInfo.create_table():
            Msg("错误", "老师信息创建错误", self).show()
        if not CourseInfo.create_table():
            Msg("错误", "课程信息创建错误", self).show()
        if not ClassInfo.create_table():
            Msg("错误", "班级信息创建错误", self).show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
