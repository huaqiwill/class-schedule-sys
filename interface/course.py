from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidgetItem,
    QHeaderView, QDialog, QApplication, QLabel, QFormLayout, QComboBox, QSpacerItem, QSizePolicy, QFileDialog,
)
from qfluentwidgets import TableWidget, LineEdit, PushButton, MessageBox, ComboBox

from common.models import CourseInfo, ClassesInfo, StudentInfo
from pubsub import pub
from common.config import PubEvent
from common.utils import csv_to_dict_list, dict_list_to_csv


class CourseManage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initWindow()
        self.__initPage()
        self.__initLayout()
        self.__initData()

        pub.subscribe(self.__initComboBox, PubEvent.CLASSES_UPDATED)

    def __initWindow(self):
        self.setObjectName("CourseManage")
        self.setStyleSheet("CourseManage{background: rgb(255, 255, 255)} ")

    def __initPage(self):
        # 表格
        self.tableLabels = ["节次", "星期一", "星期二", "星期三", "星期四", "星期五"]
        self.tableFields = ["", "WEEKDAY1", "WEEKDAY2", "WEEKDAY3", "WEEKDAY4", "WEEKDAY5"]
        self.tableView = TableWidget(self)
        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)
        self.tableView.setWordWrap(False)
        self.tableView.verticalHeader().hide()
        self.tableView.setColumnCount(len(self.tableLabels))
        self.tableView.setHorizontalHeaderLabels(self.tableLabels)
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 组合款
        self.comboBox = ComboBox(self)
        self.comboBox.currentIndexChanged.connect(self.__onClassesItemChanged)
        # 按钮
        self.btnAdd = PushButton("添加", self)
        self.btnAdd.clicked.connect(self.__onAdd)

        self.btnEdit = PushButton("编辑", self)
        self.btnEdit.clicked.connect(self.__onEdit)

        self.btnDelete = PushButton("删除", self)
        self.btnDelete.clicked.connect(self.__onDelete)

        self.btnImport = PushButton("导入", self)
        self.btnImport.clicked.connect(self.__onImport)

        self.btnExport = PushButton("导出", self)
        self.btnExport.clicked.connect(self.__onExport)

    def __onAdd(self):
        frame = CourseAddOrEdit(self, self.__getCurrentTable())
        result = frame.exec()
        if result:
            self.__initData()

    def __onEdit(self):
        selected_indexes = self.tableView.selectionModel().selectedIndexes()
        if not selected_indexes:
            MessageBox("提示", "没有选择任何行", self).exec()
            return
        selected_row = selected_indexes[0].row()
        id = self.courseList[selected_row].get("id")
        # 编辑数据
        edit_data = CourseInfo.info(self.__getCurrentTable(), id)
        print("编辑数据", edit_data)
        self.addFrame = CourseAddOrEdit(self, self.__getCurrentTable(), edit_data)
        result = self.addFrame.exec()
        print(result)
        if result:
            self.__initData()

    def __onDelete(self):
        selected_indexes = self.tableView.selectionModel().selectedIndexes()
        if not selected_indexes:
            MessageBox("提示", "没有选择任何行", self).exec()
            return
        selected_row = selected_indexes[0].row()
        id = self.courseList[selected_row].get("id")
        if CourseInfo.delete(self.__getCurrentTable(), id):
            self.__initData()
            MessageBox("提示", "删除成功", self).exec()
        else:
            MessageBox("提示", "删除失败", self).exec()

    def __getCurrentTable(self):
        return "G" + str(self.classes_list[self.comboBox.currentIndex()].get("id"))

    def __onImport(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;All Files (*)",
                                                  options=options)
        if fileName:
            print("Selected file:", fileName)
            data = csv_to_dict_list(fileName)
            for item in data:
                item.pop("id")
                CourseInfo.save(self.__getCurrentTable(), item)
                self.__initData()

    def __onExport(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv);;All Files (*)",
                                                  options=options)
        if fileName:
            print("Save file:", fileName)
            dict_list_to_csv(CourseInfo.list(self.__getCurrentTable(), 1, 10), fileName)
            print("导出成功")

    def __initData(self):
        # 初始化组合框数据
        self.__initComboBox()
        self.__initTable()

    def __initTable(self):
        class_ = self.classes_list[self.comboBox.currentIndex()]
        course_list = CourseInfo.list(self.__getCurrentTable(), 1, 10)
        # 初始化表格数据
        self.tableView.setRowCount(len(course_list))
        self.courseList = course_list
        for i, course_info in enumerate(course_list):
            self.tableView.setItem(i, 0, QTableWidgetItem("第 {} 节".format(i + 1)))
            self.tableView.setItem(i, 1, QTableWidgetItem(course_info.get("WEEKDAY1")))
            self.tableView.setItem(i, 2, QTableWidgetItem(course_info.get("WEEKDAY2")))
            self.tableView.setItem(i, 3, QTableWidgetItem(course_info.get("WEEKDAY3")))
            self.tableView.setItem(i, 4, QTableWidgetItem(course_info.get("WEEKDAY4")))
            self.tableView.setItem(i, 5, QTableWidgetItem(course_info.get("WEEKDAY5")))

    def __initComboBox(self):
        self.comboBox.clear()
        self.classes_list = ClassesInfo.list(1, 10)
        for classes in self.classes_list:
            self.comboBox.addItem(classes.get("name"))

    def __onClassesItemChanged(self, index):
        print("选择的班级为：", self.__getCurrentTable())
        CourseInfo.create_table(self.__getCurrentTable())
        self.__initTable()

    def __initLayout(self):
        # 水平布局
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.addWidget(self.comboBox)
        self.hBoxLayout.addWidget(self.btnAdd)
        self.hBoxLayout.addWidget(self.btnEdit)
        self.hBoxLayout.addWidget(self.btnDelete)
        self.hBoxLayout.addWidget(self.btnImport)
        self.hBoxLayout.addWidget(self.btnExport)
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hBoxLayout.addSpacerItem(spacer)
        # 垂直布局
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.tableView)


class CourseAddOrEdit(QDialog):
    def __init__(self, parent, table: str, edit_data: dict = None):
        super().__init__(parent)
        self.table = table
        self.edit_data = edit_data
        self.__initWindow()
        self.__initPage()
        self.__initLayout()
        self.__initData()

    def __initData(self):
        if self.edit_data:
            self.weekday1_edit.setText(self.edit_data.get("WEEKDAY1"))
            self.weekday2_edit.setText(self.edit_data.get("WEEKDAY2"))
            self.weekday3_edit.setText(self.edit_data.get("WEEKDAY3"))
            self.weekday4_edit.setText(self.edit_data.get("WEEKDAY4"))
            self.weekday5_edit.setText(self.edit_data.get("WEEKDAY5"))

    def __initWindow(self):
        if self.edit_data:
            self.setWindowTitle("修改课程表")
        else:
            self.setWindowTitle("添加课程表")
        self.setObjectName("CourseAddOrEdit")
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
        self.weekday1_label = QLabel("星期一")
        self.weekday1_edit = LineEdit(self)

        self.weekday2_label = QLabel("星期二")
        self.weekday2_edit = LineEdit(self)

        self.weekday3_label = QLabel("星期三")
        self.weekday3_edit = LineEdit(self)

        self.weekday4_label = QLabel("星期四")
        self.weekday4_edit = LineEdit(self)

        self.weekday5_label = QLabel("星期五")
        self.weekday5_edit = LineEdit(self)

        self.btnOk = PushButton("确定")
        self.btnOk.clicked.connect(self.__onOk)

        self.btnCancel = PushButton("取消")
        self.btnCancel.clicked.connect(self.__onCancel)

    def __initLayout(self):
        self.control_layout = QHBoxLayout()
        self.control_layout.addWidget(self.btnOk)
        self.control_layout.addWidget(self.btnCancel)

        self.vbox = QFormLayout()
        self.vbox.addRow(self.weekday1_label, self.weekday1_edit)
        self.vbox.addRow(self.weekday2_label, self.weekday2_edit)
        self.vbox.addRow(self.weekday3_label, self.weekday3_edit)
        self.vbox.addRow(self.weekday4_label, self.weekday4_edit)
        self.vbox.addRow(self.weekday5_label, self.weekday5_edit)
        self.vbox.addRow(self.control_layout)

        self.setLayout(self.vbox)

    def __onCancel(self):
        self.close()
        self.reject()

    def __onOk(self):
        cls = {
            "WEEKDAY1": self.weekday1_edit.text(),
            "WEEKDAY2": self.weekday2_edit.text(),
            "WEEKDAY3": self.weekday3_edit.text(),
            "WEEKDAY4": self.weekday4_edit.text(),
            "WEEKDAY5": self.weekday5_edit.text(),
        }

        if self.edit_data:
            cls["id"] = self.edit_data.get("id")

        print(cls)
        print("当前的表", self.table)
        if ClassesInfo.save(self.table, cls):
            self.close()
            self.accept()
        MessageBox("提示", "保存失败", self).show()
