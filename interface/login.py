import sys

import PySide6
from PySide6.QtCore import *
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import *


class LoginInterface(QDialog):
    def __init__(self, parent=None):
        super(LoginInterface, self).__init__(parent)
        self.__loginNow = False
        self.__initWindow()
        self.__initPage()
        self.__initLayout()
        self.__initData()

    def __initPage(self):
        self.username_label = QLabel()
        self.username_label.setObjectName("username_label")

        self.username_edit = QLineEdit()
        self.username_edit.setObjectName("username_edit")
        self.username_edit.setPlaceholderText("请输入用户名")

        self.password_label = QLabel()
        self.password_label.setObjectName("password_label")

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText("请输入密码")
        self.password_edit.setObjectName("password_edit")

        self.role_label = QLabel()
        self.role_label.setObjectName("role_label")

        self.role_comboBox = QComboBox()
        self.role_comboBox.addItem("")
        self.role_comboBox.addItem("")
        self.role_comboBox.addItem("")
        self.role_comboBox.setObjectName("role_comboBox")
        self.role_comboBox.currentIndexChanged.connect(self.__onRoleChanged)

        self.loginBtn = QPushButton(self)
        self.loginBtn.setObjectName("loginBtn")
        self.loginBtn.setGeometry(QRect(60, 110, 371, 28))
        self.loginBtn.clicked.connect(self.__onLogin)

        self.__reTranslateUI()
        QMetaObject.connectSlotsByName(self)

    def __onRoleChanged(self, index):
        if index == 0:
            self.username_edit.setText("admin")
            self.password_edit.setText("admin")
        else:
            self.username_edit.setText("")
            self.password_edit.setText("")

    def __onLogin(self):
        self.__loginNow = True
        loginForm = {
            "username": self.username_edit.text(),
            "password": self.password_edit.text()
        }

        if loginForm.get("username") in (None, ""):
            return QMessageBox.information(self, "提示", "请输入用户名")
        if loginForm.get("password") in (None, ""):
            return QMessageBox.information(self, "提示", "请输入密码")

        if self.role_comboBox.currentText() == "管理员":
            print("管理员")
            if loginForm.get("username") == "admin" and loginForm.get("password") == "admin":
                self.close()
                self.accept()
            else:
                return QMessageBox.information(self, "提示", "用户名或密码错误")
        if self.role_comboBox.currentText() == "老师":
            print("老师")
            return QMessageBox.information(self, "提示", "用户名或密码错误")
        if self.role_comboBox.currentText() == "学生":
            print("学生")
            return QMessageBox.information(self, "提示", "用户名或密码错误")

    def __reTranslateUI(self):
        self.setWindowTitle(
            QCoreApplication.translate("Form", "\u7528\u6237\u767b\u5f55", None)
        )
        self.username_label.setText(
            QCoreApplication.translate("Form", "\u7528\u6237\u540d", None)
        )
        self.password_label.setText(QCoreApplication.translate("Form", "\u5bc6\u7801", None))
        self.role_label.setText(QCoreApplication.translate("Form", "\u89d2\u8272", None))
        self.role_comboBox.setItemText(
            0, QCoreApplication.translate("Form", "\u7ba1\u7406\u5458", None)
        )
        self.role_comboBox.setItemText(
            1, QCoreApplication.translate("Form", "\u8001\u5e08", None)
        )
        self.role_comboBox.setItemText(
            2, QCoreApplication.translate("Form", "\u5b66\u751f", None)
        )
        self.loginBtn.setText(
            QCoreApplication.translate("Form", "\u767b\u5f55", None)
        )

    def __initWindow(self):
        self.resize(440, 154)
        self.setObjectName("Form")

    def closeEvent(self, arg__1: QCloseEvent) -> None:
        if not self.__loginNow:
            sys.exit(0)

    def __initLayout(self):
        self.formLayoutWidget = QWidget(self)
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 10, 421, 91))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName("formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.addRow(self.username_label, self.username_edit)
        self.formLayout.addRow(self.password_label, self.password_edit)
        self.formLayout.addRow(self.role_label, self.role_comboBox)

    def __initData(self):
        self.username_edit.setText("admin")
        self.password_edit.setText("admin")
