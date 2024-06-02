from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_LoginForm(QWidget):
    def setupUi(self):
        if not self.objectName():
            self.setObjectName("Form")
        self.resize(440, 154)
        self.formLayoutWidget = QWidget(self)
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 10, 421, 91))
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

        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setGeometry(QRect(60, 110, 371, 28))

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(
            QCoreApplication.translate("Form", "\u7528\u6237\u767b\u5f55", None)
        )
        self.label.setText(
            QCoreApplication.translate("Form", "\u7528\u6237\u540d", None)
        )
        self.label_2.setText(QCoreApplication.translate("Form", "\u5bc6\u7801", None))
        self.label_3.setText(QCoreApplication.translate("Form", "\u89d2\u8272", None))
        self.comboBox.setItemText(
            0, QCoreApplication.translate("Form", "\u7ba1\u7406\u5458", None)
        )
        self.comboBox.setItemText(
            1, QCoreApplication.translate("Form", "\u8001\u5e08", None)
        )
        self.comboBox.setItemText(
            2, QCoreApplication.translate("Form", "\u5b66\u751f", None)
        )

        self.pushButton_2.setText(
            QCoreApplication.translate("Form", "\u767b\u5f55", None)
        )
