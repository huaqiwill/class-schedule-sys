from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidgetItem,
    QHeaderView, QDialog, QApplication, QLabel, QFormLayout,
)
from qfluentwidgets import TableWidget, LineEdit, PushButton, MessageBox

from common.models import CourseInfo


class CourseManage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initWindow()
        self.__initPage()
        self.__initLayout()
        self.__initData()

    def __initWindow(self):
        self.setObjectName("CourseManage")
        self.setStyleSheet("CourseManage{background: rgb(255, 255, 255)} ")

    def __initPage(self):
        # 表格
        self.tableLabels = ["节次", "星期一", "星期二", "星期三", "星期四", "星期五"]
        self.tableView = TableWidget(self)
        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)
        self.tableView.setWordWrap(False)
        self.tableView.verticalHeader().hide()
        self.tableView.setColumnCount(len(self.tableLabels))
        self.tableView.setHorizontalHeaderLabels(self.tableLabels)
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.itemChanged.connect(self.__onItemChanged)

    def __initData(self):
        course_list = CourseInfo.course_page(1, 10)
        self.tableView.setRowCount(len(course_list))
        self.tableView.raw = course_list
        for i, course_info in enumerate(course_list):
            self.tableView.setItem(i, 0, QTableWidgetItem("第 {} 节".format(i + 1)))
            self.tableView.setItem(i, 1, QTableWidgetItem(course_info.get("WEEKDAY1")))
            self.tableView.setItem(i, 2, QTableWidgetItem(course_info.get("WEEKDAY2")))
            self.tableView.setItem(i, 3, QTableWidgetItem(course_info.get("WEEKDAY3")))
            self.tableView.setItem(i, 4, QTableWidgetItem(course_info.get("WEEKDAY4")))
            self.tableView.setItem(i, 5, QTableWidgetItem(course_info.get("WEEKDAY5")))

    def __onItemChanged(self, item: QTableWidgetItem):
        row, column = item.row(), item.column()
        label = self.tableLabels[column]
        print(label)
        data = self.tableView.raw[row]
        print(data)
        data[label] = item.text()
        print(data)

    def __initLayout(self):
        # 水平布局
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.tableView)


class CourseAddOrEdit(QDialog):
    def __init__(self, parent=None, edit_data: dict = None):
        super().__init__(parent)
        self.__initWindow()
        self.__initPage()
        self.__initLayout()
        self.__initData()
        self.edit_data = edit_data

    def __initData(self):
        if self.edit_data:
            self.stu_name_edit.setText(self.edit_data.get("stu_name"))

    def __initWindow(self):
        self.setWindowTitle("添加学生")
        self.setObjectName("StudentAddOrEdit")
        self.resize(300, 200)  # 设置窗口的初始大小
        self.__center_screen()

    def __center_screen(self):
        # 获取屏幕尺寸
        app = QApplication.instance()
        screen = app.primaryScreen().availableGeometry()
        # 计算窗口应放置的位置以居中
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2

        # 设置窗口的位置
        self.move(x, y)

    def __initPage(self):
        self.stu_name_label = QLabel("学生姓名")
        self.stu_name_edit = LineEdit(self)

        self.stu_gradle_label = QLabel("年级")
        self.stu_gradle_edit = LineEdit(self)

        self.stu_marjor_label = QLabel("专业")
        self.stu_marjor_edit = LineEdit(self)

        self.stu_classes_label = QLabel("班级")
        self.stu_classes_edit = LineEdit(self)

        self.btnOk = PushButton("确定")
        self.btnOk.clicked.connect(self.__ev_ok)

        self.btnCancel = PushButton("取消")
        self.btnCancel.clicked.connect(self.__ev_cancel)

    def __initLayout(self):
        self.control_layout = QHBoxLayout()
        self.control_layout.addWidget(self.btnOk)
        self.control_layout.addWidget(self.btnCancel)

        self.vbox = QFormLayout()
        self.vbox.addRow(self.stu_name_label, self.stu_name_edit)
        self.vbox.addRow(self.stu_gradle_label, self.stu_gradle_edit)
        self.vbox.addRow(self.stu_marjor_label, self.stu_marjor_edit)
        self.vbox.addRow(self.stu_classes_label, self.stu_classes_edit)
        self.vbox.addRow(self.control_layout)

        self.setLayout(self.vbox)

    def __ev_cancel(self):
        self.close()

    def __ev_ok(self):
        student = {
            "name": self.stu_name_edit.text(),
            "grade": self.stu_gradle_edit.text(),
            "class_name": self.stu_classes_edit.text(),
            "major": self.stu_marjor_edit.text(),
        }

        if student.get("name") in (None, ""):
            return MessageBox("提示", "学生姓名不能为空", self).show()
        if student.get("grade") in (None, ""):
            return MessageBox("提示", "学生年级不能为空", self).show()
        if student.get("class_name") in (None, ""):
            return MessageBox("提示", "学生班级不能为空", self).show()
        if student.get("major") in (None, ""):
            return MessageBox("提示", "学生专业不能为空", self).show()

        if self.edit_data:
            student["id"] = self.edit_data.get("id")

        print(student)

        if ClassesInfo.save(student):
            self.close()
        MessageBox("提示", "保存失败", self).show()
