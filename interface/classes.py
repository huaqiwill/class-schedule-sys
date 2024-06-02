# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QRect, QCoreApplication, QMetaObject
from PySide6.QtWidgets import (
    QWidget,
    QFormLayout, QHBoxLayout, QSizePolicy, QSpacerItem, QHeaderView, QVBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QDialog, QApplication, QTableWidgetItem,
)
from qfluentwidgets import (
    TableWidget,
    MessageBox,
    PushButton,
    LineEdit,
)
from common.models import TeacherInfo, ClassesInfo


class ClassManage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initWindow()
        self.__initPage()
        self.__initLayout()
        self.__initData()

    def __initWindow(self):
        self.setObjectName("ClassManage")
        self.setStyleSheet("ClassManage{background: rgb(255, 255, 255)} ")

    def __initPage(self):
        # 添加
        self.btnAdd = PushButton("添加", self)
        self.btnAdd.setMaximumWidth(150)
        self.btnAdd.clicked.connect(self.__onClassesAdd)

        # 删除
        self.btnDel = PushButton("删除", self)
        self.btnDel.setMaximumWidth(150)
        self.btnDel.clicked.connect(self.__onClassesDelete)

        # 编辑
        self.btnEdit = PushButton("编辑", self)
        self.btnEdit.setMaximumWidth(150)
        self.btnEdit.clicked.connect(self.__onClassesEdit)

        # 导入
        self.btnImport = PushButton("导入", self)
        self.btnImport.setMaximumWidth(150)
        self.btnImport.clicked.connect(self.__onClassesImport)

        # 导出
        self.btnExport = PushButton("导出", self)
        self.btnExport.setMaximumWidth(150)
        self.btnExport.clicked.connect(self.__onClassesExport)

        # 表格
        header_labels = ["老师姓名", "手机号"]
        self.tableView = TableWidget(self)
        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)
        self.tableView.setWordWrap(False)
        self.tableView.verticalHeader().hide()
        self.tableView.setColumnCount(len(header_labels))
        self.tableView.setHorizontalHeaderLabels(header_labels)
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def __initData(self):
        result_list = TeacherInfo.list(1, 10)
        self.tableView.setRowCount(len(result_list))
        for i, result in enumerate(result_list):
            self.tableView.setItem(i, 0, QTableWidgetItem(result.get("name")))
            self.tableView.setItem(i, 1, QTableWidgetItem(result.get("phone")))
            # self.tableView.setItem(i, 2, QTableWidgetItem(result.get("password")))

    def __initLayout(self):
        # 水平布局
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.addWidget(self.btnAdd)
        self.hBoxLayout.addWidget(self.btnDel)
        self.hBoxLayout.addWidget(self.btnImport)
        self.hBoxLayout.addWidget(self.btnExport)
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hBoxLayout.addSpacerItem(spacer)
        # 垂直布局
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.tableView)

    def __onClassesAdd(self):
        self.add_frame = ClassAddOrEdit(self)
        self.add_frame.show()

    def __onClassesDelete(self):
        pass

    def __onClassesImport(self):
        pass

    def __onClassesExport(self):
        pass

    def __onClassesEdit(self):
        pass


class ClassAddOrEdit(QDialog):
    def __init__(self, parent=None, edit_data: dict = None):
        super().__init__(parent)
        self.__initWindow()
        self.__initPage()
        self.__initLayout()
        self.__initData()
        self.edit_data = edit_data

    def __initLayout(self):
        self.control_layout = QHBoxLayout()
        self.control_layout.addWidget(self.btnOk)
        self.control_layout.addWidget(self.btnCancel)

        self.vbox = QFormLayout()
        self.vbox.addRow(self.stu_name_label, self.name_edit)
        self.vbox.addRow(self.stu_gradle_label, self.stu_gradle_edit)
        self.vbox.addRow(self.stu_marjor_label, self.stu_marjor_edit)
        self.vbox.addRow(self.stu_classes_label, self.stu_classes_edit)
        self.vbox.addRow(self.control_layout)

        self.setLayout(self.vbox)

    def __initData(self):
        if self.edit_data:
            self.name_edit.setText(self.edit_data.get("name"))
            self.name_edit.setText(self.edit_data.get("teacher"))
            self.name_edit.setText(self.edit_data.get("phone"))
            self.name_edit.setText(self.edit_data.get("password"))
            self.name_edit.setText(self.edit_data.get("classes"))

    def __initWindow(self):
        self.setWindowTitle("添加学生")
        self.setObjectName("StudentAddOrEdit")
        self.resize(300, 200)  # 设置窗口的初始大小
        self.__centerScreen()

    def __centerScreen(self):
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
        self.name_edit = LineEdit(self)

        self.stu_gradle_label = QLabel("年级")
        self.stu_gradle_edit = LineEdit(self)

        self.stu_marjor_label = QLabel("专业")
        self.stu_marjor_edit = LineEdit(self)

        self.stu_classes_label = QLabel("班级")
        self.stu_classes_edit = LineEdit(self)

        self.btnOk = PushButton("确定")
        self.btnOk.clicked.connect(self.__onOk)

        self.btnCancel = PushButton("取消")
        self.btnCancel.clicked.connect(self.__onCancel)

    def __onCancel(self):
        self.close()
        self.reject()

    def __onOk(self):
        classes = {
            "name": self.name_edit.text(),
            "grade": self.stu_gradle_edit.text(),
            "class_name": self.stu_classes_edit.text(),
            "major": self.stu_marjor_edit.text(),
        }

        if classes.get("name") in (None, ""):
            return MessageBox("提示", "学生姓名不能为空", self).show()
        if classes.get("grade") in (None, ""):
            return MessageBox("提示", "学生年级不能为空", self).show()
        if classes.get("class_name") in (None, ""):
            return MessageBox("提示", "学生班级不能为空", self).show()
        if classes.get("major") in (None, ""):
            return MessageBox("提示", "学生专业不能为空", self).show()

        if self.edit_data:
            classes["id"] = self.edit_data.get("id")

        print(classes)

        if ClassesInfo.save(classes):
            self.close()
            self.accept()
        MessageBox("提示", "保存失败", self).show()
