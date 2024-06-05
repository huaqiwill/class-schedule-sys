import os
import sys
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from qfluentwidgets import (
    FluentWindow,
    FluentIcon as FIF, PushButton, MessageBox,
)
from interface import (
    CourseManage,
    StudentManage,
    ClassManage,
    TeacherManage, LoginInterface,
)
from common.models import AdminInfo, StudentInfo, TeacherInfo, CourseInfo, ClassesInfo
import logging
from common import config

logging.basicConfig(
    filename="./data/info.log",
    filemode="w",
    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
    datefmt="%Y-%M-%d %H:%M:%S",
    level=logging.INFO,
    encoding="utf8",
)


class MainWindow(FluentWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.role = config.role
        print("当前角色", self.role)
        self.__initWindow()
        self.__initNavigation()
        self.__initData()

    def __initNavigation(self):
        if self.role == "管理员":
            self.addSubInterface(CourseManage(), QIcon("./resource/icon/课程管理.png"), "课程管理")
            self.addSubInterface(StudentManage(), QIcon("./resource/icon/学生管理.png"), "学生管理")
            self.addSubInterface(ClassManage(), QIcon("./resource/icon/班级管理.png"), "班级管理")
            self.addSubInterface(TeacherManage(), QIcon("./resource/icon/教师管理.png"), "教师管理")
        if self.role == "老师":
            self.addSubInterface(CourseManage(), QIcon("./resource/icon/课程管理.png"), "课程管理")
            self.addSubInterface(StudentManage(), QIcon("./resource/icon/学生管理.png"), "学生管理")
            self.addSubInterface(ClassManage(), QIcon("./resource/icon/班级管理.png"), "班级管理")
        if self.role == "学生":
            self.addSubInterface(CourseManage(), QIcon("./resource/icon/课程管理.png"), "课表查看")

    def __initWindow(self):
        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)
        self.setCustomBackgroundColor(QColor(240, 244, 249), QColor(32, 32, 32))
        self.setWindowIcon(QIcon("./resource/icon/student.png"))
        self.resize(800, 600)
        self.setWindowTitle("学生课表系统")

    def __initData(self):
        logging.info("创建数据表，如果不存在")
        if not AdminInfo.create_table():
            logging.error("管理员表创建失败")
        if not StudentInfo.create_table():
            logging.info("学生表创建失败")
        if not TeacherInfo.create_table():
            logging.info("老师表创建失败")
        if not ClassesInfo.create_table():
            logging.info("班级表创建失败")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./resource/icon/student.png"))

    login = LoginInterface()
    if not login.exec():
        sys.exit(0)

    w = MainWindow()
    w.show()
    sys.exit(app.exec())
