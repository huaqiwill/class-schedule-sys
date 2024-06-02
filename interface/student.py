# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QRect, QCoreApplication, QMetaObject
from PySide6.QtWidgets import (
    QWidget,
    QFormLayout, QHBoxLayout, QSizePolicy, QSpacerItem, QHeaderView, QVBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QDialog, QApplication, QTableWidgetItem, QFileDialog,
)
from qfluentwidgets import (
    TableWidget,
    MessageBox,
    PushButton,
    LineEdit, FluentIcon,
)
from common.models import StudentInfo
from common.utils import csv_to_dict_list, dict_list_to_csv


class StudentManage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initWindow()
        self.__initPage()
        self.__initData()
        self.__initLayout()

    def __initWindow(self):
        self.setObjectName("StudentManage")
        self.setStyleSheet("StudentManage{background: rgb(255, 255, 255)} ")

    def __initPage(self):
        # 添加
        self.btnAdd = PushButton("添加", self)
        self.btnAdd.setMaximumWidth(150)
        self.btnAdd.clicked.connect(self.__onStudentAdd)

        # 删除
        self.btnDel = PushButton("删除", self)
        self.btnDel.setMaximumWidth(150)
        self.btnDel.clicked.connect(self.__onStudentDelete)

        # 编辑
        self.btnEdit = PushButton("编辑", self)
        self.btnEdit.setMaximumWidth(150)
        self.btnEdit.clicked.connect(self.__onStudentEdit)

        # 导入
        self.btnImport = PushButton("导入", self)
        self.btnImport.setMaximumWidth(150)
        self.btnImport.clicked.connect(self.__onStudentImport)

        # 导出
        self.btnExport = PushButton("导出", self)
        self.btnExport.setMaximumWidth(150)
        self.btnExport.clicked.connect(self.__onStudentExport)

        # 表格
        header_labels = ["ID（学号）", "姓名", "年级", "专业", "班级"]
        self.tableView = TableWidget(self)
        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)
        self.tableView.setWordWrap(False)
        self.tableView.verticalHeader().hide()
        self.tableView.setColumnCount(len(header_labels))
        self.tableView.setHorizontalHeaderLabels(header_labels)
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def __initLayout(self):
        # 水平布局
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.addWidget(self.btnAdd)
        self.hBoxLayout.addWidget(self.btnDel)
        self.hBoxLayout.addWidget(self.btnEdit)
        self.hBoxLayout.addWidget(self.btnImport)
        self.hBoxLayout.addWidget(self.btnExport)
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hBoxLayout.addSpacerItem(spacer)
        # 垂直布局
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.tableView)

    def __initData(self):
        result_list = StudentInfo.list(1, 50)
        print(result_list)
        self.tableView.setRowCount(len(result_list))
        for i, result in enumerate(result_list):
            self.tableView.setItem(i, 0, QTableWidgetItem(str(result.get("id"))))
            self.tableView.setItem(i, 1, QTableWidgetItem(result.get("name")))
            self.tableView.setItem(i, 2, QTableWidgetItem(result.get("grade")))
            self.tableView.setItem(i, 3, QTableWidgetItem(result.get("major")))
            self.tableView.setItem(i, 4, QTableWidgetItem(result.get("class_num")))

    def __onStudentAdd(self):
        self.add_frame = StudentAddOrEdit(self)
        result = self.add_frame.exec()
        print(result)
        if result:
            self.__initData()

    def __onStudentDelete(self):
        selected_indexes = self.tableView.selectionModel().selectedIndexes()
        if not selected_indexes:
            MessageBox("提示", "没有选择任何行", self).exec()
            return
        selected_row = selected_indexes[0].row()
        selected_item = self.tableView.item(selected_row, 0)
        id = int(selected_item.text())
        print(id)
        if StudentInfo.delete(id):
            self.__initData()
            MessageBox("提示", "删除成功", self).exec()
        else:
            MessageBox("提示", "删除失败", self).exec()

    def __onStudentImport(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;All Files (*)",
                                                  options=options)
        if fileName:
            print("Selected file:", fileName)
            data = csv_to_dict_list(fileName)
            for item in data:
                item.pop("id")
                StudentInfo.save(item)
                self.__initData()

    def __onStudentExport(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv);;All Files (*)",
                                                  options=options)
        if fileName:
            print("Save file:", fileName)
            dict_list_to_csv(StudentInfo.list(1, 10), fileName)
            print("导出成功")

    def __onStudentEdit(self):
        selected_indexes = self.tableView.selectionModel().selectedIndexes()
        if not selected_indexes:
            MessageBox("提示", "没有选择任何行", self).exec()
            return
        selected_row = selected_indexes[0].row()
        selected_item = self.tableView.item(selected_row, 0)
        id = int(selected_item.text())
        edit_data = StudentInfo.info(id)
        self.add_frame = StudentAddOrEdit(self, edit_data)
        result = self.add_frame.exec()
        print(result)
        if result:
            self.__initData()


class StudentAddOrEdit(QDialog):
    def __init__(self, parent=None, edit_data: dict = None):
        super().__init__(parent)
        self.__initWindow()
        self.__initPage()
        self.__initLayout()
        self.__initData()
        self.edit_data = edit_data

    def __initData(self):
        if self.edit_data:
            self.stu_name_edit.setText(self.edit_data.get("name"))
            self.stu_gradle_edit.setText(self.edit_data.get("grade"))
            self.stu_marjor_edit.setText(self.edit_data.get("major"))
            self.stu_classes_edit.setText(self.edit_data.get("class_num"))

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

    def __initLayout(self):
        # 控制盒子
        self.control_layout = QHBoxLayout()
        self.control_layout.addWidget(self.btnOk)
        self.control_layout.addWidget(self.btnCancel)
        # 表单布局
        self.vbox = QFormLayout()
        self.vbox.addRow(self.stu_name_label, self.stu_name_edit)
        self.vbox.addRow(self.stu_gradle_label, self.stu_gradle_edit)
        self.vbox.addRow(self.stu_marjor_label, self.stu_marjor_edit)
        self.vbox.addRow(self.stu_classes_label, self.stu_classes_edit)
        self.vbox.addRow(self.control_layout)
        self.setLayout(self.vbox)

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
        self.btnOk.clicked.connect(self.__onOk)

        self.btnCancel = PushButton("取消")
        self.btnCancel.clicked.connect(self.__onCancel)

    def __onCancel(self):
        self.close()
        super().reject()

    def __onOk(self):
        student = {
            "name": self.stu_name_edit.text(),
            "grade": self.stu_gradle_edit.text(),
            "class_num": self.stu_classes_edit.text(),
            "major": self.stu_marjor_edit.text(),
        }

        if student.get("name") in (None, ""):
            return MessageBox("提示", "学生姓名不能为空", self).show()
        if student.get("grade") in (None, ""):
            return MessageBox("提示", "学生年级不能为空", self).show()
        if student.get("class_num") in (None, ""):
            return MessageBox("提示", "学生班级不能为空", self).show()
        if student.get("major") in (None, ""):
            return MessageBox("提示", "学生专业不能为空", self).show()

        if self.edit_data:
            student["id"] = self.edit_data.get("id")

        print(student)
        if StudentInfo.save(student):
            self.close()
            super().accept()
        MessageBox("提示", "保存失败", self).show()
