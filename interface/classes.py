# This Python file uses the following encoding: utf-8
from datetime import datetime

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
    LineEdit, ComboBox,
)
from common.models import TeacherInfo, ClassesInfo, CourseInfo
from common.utils import csv_to_dict_list, dict_list_to_csv
from pubsub import pub
from common.config import PubEvent


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
        header_labels = ["ID（班级编号）", "班级名称", "教师姓名", "上课地点"]
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
        result_list = ClassesInfo.list(1, 10)
        self.tableView.setRowCount(len(result_list))
        for i, result in enumerate(result_list):
            self.tableView.setItem(i, 0, QTableWidgetItem(str(result.get("id"))))
            self.tableView.setItem(i, 1, QTableWidgetItem(result.get("name")))
            self.tableView.setItem(i, 2, QTableWidgetItem(result.get("teacher")))
            self.tableView.setItem(i, 3, QTableWidgetItem(result.get("place")))

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

    def __onClassesAdd(self):
        self.add_frame = ClassesAddOrEdit(self)
        result = self.add_frame.exec()
        if result:
            self.__initData()
            pub.sendMessage(PubEvent.CLASSES_UPDATED)

    def __onClassesDelete(self):
        selected_indexes = self.tableView.selectionModel().selectedIndexes()
        if not selected_indexes:
            MessageBox("提示", "没有选择任何行", self).exec()
            return
        selected_row = selected_indexes[0].row()
        selected_item = self.tableView.item(selected_row, 0)
        id = int(selected_item.text())
        print(id)
        if ClassesInfo.delete(id):
            self.__initData()
            pub.sendMessage(PubEvent.CLASSES_UPDATED)
            MessageBox("提示", "删除成功", self).exec()
        else:
            MessageBox("提示", "删除失败", self).exec()

    def __onClassesImport(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;All Files (*)",
                                                  options=options)
        if fileName:
            print("Selected file:", fileName)
            data = csv_to_dict_list(fileName)
            for item in data:
                item.pop("id")
                ClassesInfo.save(item)
                self.__initData()

            MessageBox("提示", "导入成功", self).exec()

    def __onClassesExport(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv);;All Files (*)",
                                                  options=options)
        if fileName:
            print("Save file:", fileName)
            dict_list_to_csv(ClassesInfo.list(1, 10), fileName)
            print("导出成功")

    def __onClassesEdit(self):
        selected_indexes = self.tableView.selectionModel().selectedIndexes()
        if not selected_indexes:
            MessageBox("提示", "没有选择任何行", self).exec()
            return
        selected_row = selected_indexes[0].row()
        selected_item = self.tableView.item(selected_row, 0)
        id = int(selected_item.text())
        edit_data = ClassesInfo.info(id)
        print("编辑数据", edit_data)
        self.add_frame = ClassesAddOrEdit(self, edit_data)
        result = self.add_frame.exec()
        print(result)
        if result:
            self.__initData()
            pub.sendMessage(PubEvent.CLASSES_UPDATED)


class ClassesAddOrEdit(QDialog):
    def __init__(self, parent=None, edit_data: dict = None):
        super().__init__(parent)
        self.edit_data = edit_data
        self.__initWindow()
        self.__initPage()
        self.__initLayout()
        self.__initData()

    def __initLayout(self):
        self.control_layout = QHBoxLayout()
        self.control_layout.addWidget(self.btnOk)
        self.control_layout.addWidget(self.btnCancel)

        self.vbox = QFormLayout()
        self.vbox.addRow(self.name_label, self.name_edit)
        self.vbox.addRow(self.teacher_label, self.teacher_combo)
        self.vbox.addRow(self.place_label, self.place_edit)
        self.vbox.addRow(self.control_layout)

        self.setLayout(self.vbox)

    def __initData(self):
        self.teachers = TeacherInfo.list(1, 10)
        for teacher in self.teachers:
            self.teacher_combo.addItem(teacher.get("name"))
        if self.edit_data:
            self.name_edit.setText(self.edit_data.get("name"))
            self.teacher_combo.setCurrentText(self.edit_data.get("teacher"))
            self.place_edit.setText(self.edit_data.get("place"))

    def __initWindow(self):
        self.setWindowTitle("添加班级")
        self.setObjectName("ClassesAddOrEdit")
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
        self.name_label = QLabel("班级名称")
        self.name_edit = LineEdit(self)
        self.name_edit.setPlaceholderText("请输入班级名称")

        self.teacher_label = QLabel("老师")
        self.teacher_combo = ComboBox(self)
        self.teacher_combo.setPlaceholderText("请输入老师姓名")

        self.place_label = QLabel("上课地点")
        self.place_edit = LineEdit(self)
        self.place_edit.setPlaceholderText("请输入上课地点")

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
            "teacher": self.teacher_combo.text(),
            "place": self.place_edit.text(),
        }

        if classes.get("name") in (None, ""):
            return MessageBox("提示", "班级名称不能为空", self).show()
        if classes.get("teacher") in (None, ""):
            return MessageBox("提示", "教师不能为空", self).show()
        if classes.get("place") in (None, ""):
            return MessageBox("提示", "上课地点不能为空", self).show()

        if self.edit_data:
            classes["id"] = self.edit_data.get("id")

        # 获取当前时间
        current_time = datetime.now()
        # 格式化时间（可选）
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        classes["time"] = formatted_time
        print("待保存数据：", classes)

        if ClassesInfo.save(classes):
            self.close()
            self.accept()
        MessageBox("提示", "保存失败", self).show()
