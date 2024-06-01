# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
)
from qfluentwidgets import (
    TableWidget,
    MessageBox,
    PushButton,
    LineEdit,
)
from common.models import StudentInfo
from PySide6.QtCore import *
from PySide6.QtWidgets import *


class StudentManage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__init_window()
        self.__init_page()
        self.__init_data()

    def __init_window(self):
        self.setObjectName("StudentManage")
        self.setStyleSheet("StudentManage{background: rgb(255, 255, 255)} ")

    def __init_page(self):
        # 添加
        self.btnAdd = PushButton("添加")
        self.btnAdd.setMaximumWidth(150)
        self.btnAdd.clicked.connect(self.__ev_stu_add)

        # 删除
        self.btnDel = PushButton("删除")
        self.btnDel.setMaximumWidth(150)
        self.btnDel.clicked.connect(self.__ev_stu_del)

        # 导入
        self.btnImport = PushButton("导入")
        self.btnImport.setMaximumWidth(150)
        self.btnImport.clicked.connect(self.__ev_stu_import)

        # 导出
        self.btnExport = PushButton("导出")
        self.btnExport.setMaximumWidth(150)
        self.btnExport.clicked.connect(self.__ev_stu_export)

        # 水平布局
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.addWidget(self.btnAdd)
        self.hBoxLayout.addWidget(self.btnDel)
        self.hBoxLayout.addWidget(self.btnImport)
        self.hBoxLayout.addWidget(self.btnExport)
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hBoxLayout.addSpacerItem(spacer)

        # 表格
        self.tableView = TableWidget(self)
        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)
        self.tableView.setWordWrap(False)
        self.tableView.verticalHeader().hide()
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 垂直布局
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.tableView)

    def __init_data(self):
        table_fields = [
            "id",
            "name",
            "sex",
            "age",
            "class_id",
            "grade_id",
            "phone",
            "address",
        ]
        raw_fields = ["学生姓名", "学号", "年龄", "性别"]
        result_list, field_names = StudentInfo.list(1, 10)
        print(field_names, result_list)
        data_size = len(result_list)
        size = len(field_names)
        self.tableView.setRowCount(data_size)
        self.tableView.setColumnCount(size)
        self.tableView.setHorizontalHeaderLabels(field_names)
        for i, result in enumerate(result_list):
            for j in range(size):
                field = field_names[j]
                self.tableView.setItem(i, j, QTableWidgetItem(result.get(field)))

    def __ev_stu_add(self):
        self.add_frame = StudentAdd(self)
        self.add_frame.show()
        

    def __ev_stu_del(self):
        pass

    def __ev_stu_import(self):
        pass

    def __ev_stu_export(self):
        pass

    def __ev_stu_edit(self):
        pass


class StudentAdd2(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.resize(435, 172)
        self.formLayoutWidget = QWidget(Form)
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 10, 421, 151))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName("formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.lineEdit = QLineEdit(self.formLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit)

        self.label_2 = QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.lineEdit_2 = QLineEdit(self.formLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_2)

        self.label_3 = QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.comboBox = QComboBox(self.formLayoutWidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName("comboBox")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboBox)

        self.label_4 = QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.comboBox_2 = QComboBox(self.formLayoutWidget)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName("comboBox_2")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.comboBox_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_3 = QPushButton(self.formLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton(self.formLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(
            QCoreApplication.translate("Form", "\u6dfb\u52a0\u5b66\u751f", None)
        )
        self.label.setText(QCoreApplication.translate("Form", "\u59d3\u540d", None))
        self.label_2.setText(QCoreApplication.translate("Form", "\u5e74\u7ea7", None))
        self.label_3.setText(QCoreApplication.translate("Form", "\u4e13\u4e1a", None))
        self.comboBox.setItemText(
            0, QCoreApplication.translate("Form", "\u7ba1\u7406\u5458", None)
        )
        self.comboBox.setItemText(
            1, QCoreApplication.translate("Form", "\u8001\u5e08", None)
        )
        self.comboBox.setItemText(
            2, QCoreApplication.translate("Form", "\u5b66\u751f", None)
        )

        self.label_4.setText(QCoreApplication.translate("Form", "\u73ed\u7ea7", None))
        self.comboBox_2.setItemText(
            0, QCoreApplication.translate("Form", "\u7ba1\u7406\u5458", None)
        )
        self.comboBox_2.setItemText(
            1, QCoreApplication.translate("Form", "\u8001\u5e08", None)
        )
        self.comboBox_2.setItemText(
            2, QCoreApplication.translate("Form", "\u5b66\u751f", None)
        )

        self.pushButton_3.setText(
            QCoreApplication.translate("Form", "\u786e\u5b9a", None)
        )
        self.pushButton_2.setText(
            QCoreApplication.translate("Form", "\u53d6\u6d88", None)
        )

    # retranslateUi


class StudentAdd(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__init_window()
        self.__init_page()
        self.__init_data()

    def __init_data(self):
        pass

    def __init_window(self):
        self.setWindowTitle("添加学生")
        self.setObjectName("StudentAdd")
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

    def __init_page(self):
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

        print(student)
        if StudentInfo.save(student):
            self.close()
        MessageBox("提示", "保存失败", self).show()
