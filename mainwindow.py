import sys
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
)
from qfluentwidgets import (
    FluentWindow,
    FluentIcon as FIF,
)
from class_schedule import (
    CourseManage,
    StudentManage,
    ClassManage,
    TeacherManage,
)
from common.models import AdminInfo, StudentInfo, TeacherInfo, CourseInfo, ClassInfo
import logging
from common.utils import DBUtils

logging.basicConfig(filename="info.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%Y-%M-%d %H:%M:%S", level=logging.INFO, encoding="utf8")


class MainWindow(FluentWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_window()

        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)
        self.setCustomBackgroundColor(QColor(240, 244, 249), QColor(32, 32, 32))

        self.course_manage = CourseManage(self)
        self.course_manage.setObjectName("course_manage")
        self.student_manage = StudentManage(self)
        self.student_manage.setObjectName("student_manage")
        self.class_manage = ClassManage(self)
        self.class_manage.setObjectName("class_manage")
        self.teacher_manage = TeacherManage(self)
        self.teacher_manage.setObjectName("teacher_manage")

        # add items to navigation interface
        self.init_navigation()
        self.init_data()

    def init_navigation(self):
        self.addSubInterface(self.course_manage, FIF.PALETTE, "课程管理")
        self.addSubInterface(self.student_manage, FIF.BUS, "学生管理")
        self.addSubInterface(self.class_manage, FIF.BUS, "班级管理")
        self.addSubInterface(self.teacher_manage, FIF.BUS, "教师管理")

    def init_window(self):
        self.resize(800, 600)
        self.setWindowTitle("学生课表系统")

    def init_data(self):
        # if not AdminInfo.create_table():
        #     Msg("错误", "管理员信息创建错误", self).show()
        # if not StudentInfo.create_table():
        #     Msg("错误", "学生信息创建错误", self).show()
        # if not TeacherInfo.create_table():
        #     Msg("错误", "老师信息创建错误", self).show()
        # if not CourseInfo.create_table():
        #     Msg("错误", "课程信息创建错误", self).show()
        # if not ClassInfo.create_table():
        #     Msg("错误", "班级信息创建错误", self).show()
        logging.info("创建数据表，如果不存在")
        if not AdminInfo.create_table():
            logging.error("管理员表创建失败")
        if not StudentInfo.create_table():
            logging.info("学生表创建失败")
        if not TeacherInfo.create_table():
            logging.info("老师表创建失败")
        if not CourseInfo.create_table():
            logging.info("课程表创建失败")
        if not ClassInfo.create_table():
            logging.info("班级表创建失败")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
