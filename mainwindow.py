# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QTableWidgetItem
from PySide6.QtGui import QColor
from PySide6.QtCore import QSize
from qfluentwidgets import FluentWindow, TableWidget, SplashScreen, LineEdit
from qfluentwidgets import FluentIcon as FIF

from class_schedule.Class1Grade7Interface import Class1Grade7Interface
from class_schedule.Class2Grade7Interface import Class2Grade7Interface
from class_schedule.Class3Grade7Interface import Class3Grade7Interface
from class_schedule.Class1Grade8Interface import Class1Grade8Interface
from class_schedule.Class2Grade8Interface import Class2Grade8Interface
from class_schedule.Class3Grade8Interface import Class3Grade8Interface
from class_schedule.Class1Grade9Interface import Class1Grade9Interface
from class_schedule.Class2Grade9Interface import Class2Grade9Interface
from class_schedule.Class3Grade9Interface import Class3Grade9Interface
from class_schedule.student_manage import StudentManage
from class_schedule.class_manage import ClassManage


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
        self.class_manage = ClassManage(self)

        # add items to navigation interface
        self.initNavigation()

    def initNavigation(self):
        self.addSubInterface(self.class1_grade7_interface, FIF.BUS, "初一(1)班")
        self.addSubInterface(self.class2_grade7_interface, FIF.CAR, "初一(2)班")
        self.addSubInterface(self.class3_grade7_interface, FIF.EDUCATION, "初一(3)班")
        self.addSubInterface(self.class1_grade8_interface, FIF.IOT, "初二(1)班")
        self.addSubInterface(self.class2_grade8_interface, FIF.COPY, "初二(2)班")
        self.addSubInterface(self.class3_grade8_interface, FIF.CALENDAR, "初二(3)班")
        self.addSubInterface(self.class1_grade9_interface, FIF.CHAT, "初三(1)班")
        self.addSubInterface(self.class2_grade9_interface, FIF.FLAG, "初三(2)班")
        self.addSubInterface(self.class3_grade9_interface, FIF.PALETTE, "初三(3)班")
        self.addSubInterface(self.student_manage, FIF.ACCEPT, "学生管理")
        self.addSubInterface(self.class_manage, FIF.ACCEPT, "班级管理")

    def initWindow(self):
        self.resize(800, 600)
        self.setWindowTitle("学生课表系统")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
