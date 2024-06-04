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
    LineEdit,
)
from common.models import TeacherInfo
from common.utils import csv_to_dict_list, dict_list_to_csv


class TeacherManage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initWindow()
        self.__initPage()
        self.__initLayout()
        self.__initData()

    def __initWindow(self):
        self.setObjectName("TeacherManage")
        self.setStyleSheet("TeacherManage{background: rgb(255, 255, 255)} ")

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

    def __initPage(self):
        # 添加
        self.btnAdd = PushButton("添加", self)
        self.btnAdd.setMaximumWidth(150)
        self.btnAdd.clicked.connect(self.__onTeacherAdd)

        # 删除
        self.btnDel = PushButton("删除", self)
        self.btnDel.setMaximumWidth(150)
        self.btnDel.clicked.connect(self.__onTeacherDelete)

        # 编辑
        self.btnEdit = PushButton("编辑", self)
        self.btnEdit.setMaximumWidth(150)
        self.btnEdit.clicked.connect(self.__onTeacherEdit)

        # 导入
        self.btnImport = PushButton("导入", self)
        self.btnImport.setMaximumWidth(150)
        self.btnImport.clicked.connect(self.__onTeacherImport)

        # 导出
        self.btnExport = PushButton("导出", self)
        self.btnExport.setMaximumWidth(150)
        self.btnExport.clicked.connect(self.__onTeacherExport)

        # 表格
        header_labels = ["ID（教师编号）", "老师姓名", "手机号"]
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
        print(result_list)
        self.tableView.setRowCount(len(result_list))
        for i, result in enumerate(result_list):
            self.tableView.setItem(i, 0, QTableWidgetItem(str(result.get("id"))))
            self.tableView.setItem(i, 1, QTableWidgetItem(result.get("name")))
            self.tableView.setItem(i, 2, QTableWidgetItem(result.get("phone")))

    def __onTeacherAdd(self):
        self.add_frame = TeacherAddOrEdit(self)
        result = self.add_frame.exec()
        if result:
            self.__initData()

    def __onTeacherDelete(self):
        selected_indexes = self.tableView.selectionModel().selectedIndexes()
        if not selected_indexes:
            MessageBox("提示", "没有选择任何行", self).exec()
            return
        selected_row = selected_indexes[0].row()
        selected_item = self.tableView.item(selected_row, 0)
        id = int(selected_item.text())
        print(id)
        if TeacherInfo.delete(id):
            self.__initData()
            MessageBox("提示", "删除成功", self).exec()
        else:
            MessageBox("提示", "删除失败", self).exec()

    def __onTeacherImport(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;All Files (*)",
                                                  options=options)
        if fileName:
            print("Selected file:", fileName)
            data = csv_to_dict_list(fileName)
            for item in data:
                item.pop("id")
                TeacherInfo.save(item)
                self.__initData()

            MessageBox("提示", "导入成功", self).exec()

    def __onTeacherExport(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv);;All Files (*)",
                                                  options=options)
        if fileName:
            print("Save file:", fileName)
            dict_list_to_csv(TeacherInfo.list(1, 10), fileName)
            MessageBox("提示", "导出成功", self).exec()

    def __onTeacherEdit(self):
        selected_indexes = self.tableView.selectionModel().selectedIndexes()
        if not selected_indexes:
            MessageBox("提示", "没有选择任何行", self).exec()
            return
        selected_row = selected_indexes[0].row()
        selected_item = self.tableView.item(selected_row, 0)
        id = int(selected_item.text())
        edit_data = TeacherInfo.info(id)
        self.add_frame = TeacherAddOrEdit(self, edit_data)
        result = self.add_frame.exec()
        print(result)
        if result:
            self.__initData()


class TeacherAddOrEdit(QDialog):
    def __init__(self, parent=None, edit_data: dict = None):
        super().__init__(parent)
        self.edit_data = edit_data
        self.__initWindow()
        self.__initPage()
        self.__initLayout()
        self.__initData()

    def __initLayout(self):
        # 控制按钮
        self.control_layout = QHBoxLayout()
        self.control_layout.addWidget(self.btnOk)
        self.control_layout.addWidget(self.btnCancel)
        # 表单布局
        self.vbox = QFormLayout()
        self.vbox.addRow(self.name_label, self.name_edit)
        self.vbox.addRow(self.phone_label, self.phone_edit)
        self.vbox.addRow(self.password_label, self.password_edit)
        self.vbox.addRow(self.control_layout)
        self.setLayout(self.vbox)

    def __initData(self):
        if self.edit_data:
            self.name_edit.setText(self.edit_data.get("name"))
            self.phone_edit.setText(self.edit_data.get("phone"))

    def __initWindow(self):
        self.setWindowTitle("添加学生")
        self.setObjectName("TeacherAddOrEdit")
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
        self.name_label = QLabel("老师姓名")
        self.name_edit = LineEdit(self)

        self.phone_label = QLabel("手机号")
        self.phone_edit = LineEdit(self)

        self.password_label = QLabel("密码")
        self.password_edit = LineEdit(self)

        self.btnOk = PushButton("确定")
        self.btnOk.clicked.connect(self.__onOk)

        self.btnCancel = PushButton("取消")
        self.btnCancel.clicked.connect(self.__onCancel)

    def __onCancel(self):
        self.close()
        self.reject()

    def __onOk(self):
        teacher = {
            "name": self.name_edit.text(),
            "phone": self.phone_edit.text(),
            "password": self.password_edit.text()
        }

        if teacher.get("name") in (None, ""):
            return MessageBox("提示", "老师姓名不能为空", self).show()
        if teacher.get("phone") in (None, ""):
            return MessageBox("提示", "老师手机号不能为空", self).show()
        if teacher.get("password") in (None, ""):
            return MessageBox("提示", "密码不能为空", self).show()

        if self.edit_data:
            teacher["id"] = self.edit_data.get("id")

        print(teacher)
        if TeacherInfo.save(teacher):
            self.close()
            self.accept()
        MessageBox("提示", "保存失败", self).show()
