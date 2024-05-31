# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidgetItem,
    QHeaderView,
    QFormLayout,
    QSpacerItem,
    QSizePolicy,
    QApplication,
    QMessageBox,
)
from qfluentwidgets import TableWidget, FluentWindow
from qfluentwidgets.components.widgets.button import PushButton
from PySide6.QtSql import QSqlDatabase, QSqlQuery


class StudentManage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("Class1Grade7Interface")

        self.vBoxLayout = QVBoxLayout(self)
        self.tableView = TableWidget(self)

        self.btnAdd = PushButton("添加")
        self.btnAdd.setMaximumWidth(150)
        self.btnAdd.clicked.connect(self.stu_add)
        self.btnDel = PushButton("删除")
        self.btnDel.setMaximumWidth(150)
        self.btnShare = PushButton("分享")
        self.btnShare.setMaximumWidth(150)
        self.hBoxLayout = QHBoxLayout()

        self.hBoxLayout.addWidget(self.btnAdd)
        self.hBoxLayout.addWidget(self.btnDel)
        self.hBoxLayout.addWidget(self.btnShare)
        # 在最后一个按钮后面添加一个伸展项，使其最右边间距自适应
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hBoxLayout.addSpacerItem(spacer)
        self.vBoxLayout.addLayout(self.hBoxLayout)

        # enable border
        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)

        self.tableView.setWordWrap(False)
        self.tableView.setRowCount(9)
        self.tableView.setColumnCount(6)

        if not QSqlDatabase.contains("qt_sql_default_connection"):
            db = QSqlDatabase.addDatabase("QSQLITE", "qt_sql_default_connection")
            db.setDatabaseName("ClassSchedules.db")
            if not db.open():
                print("Failed to connect to database")
                return
        else:
            db = QSqlDatabase.database("qt_sql_default_connection")

        classInfos = []
        for i in range(1, 10):
            classInfo = ["第 {} 节".format(i)]  # 添加节次信息
            query = QSqlQuery()
            query.prepare("SELECT * FROM C1G7 WHERE ROWID = :rowid")
            query.bindValue(":rowid", i)
            if query.exec() and query.next():
                for j in range(0, 5):
                    classInfo.append(query.value(j))
                classInfos.append(classInfo)
            else:
                print("Failed to fetch data for ROWID:", i)

        for i, classInfo in enumerate(classInfos):
            for j in range(6):
                self.tableView.setItem(i, j, QTableWidgetItem(classInfo[j]))

        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(
            ["节次", "星期一", "星期二", "星期三", "星期四", "星期五"]
        )
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.setStyleSheet("Class1Grade7Interface{background: rgb(255, 255, 255)} ")
        self.vBoxLayout.addWidget(self.tableView)

    def stu_add(self):
        self.add_frame = StudentAdd()
        self.add_frame.show()

    def stu_del(self):
        pass

    def stu_modify(self):
        pass

    def stu_query(self):
        pass


class StudentAdd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setWindowTitle("添加学生")
        self.setObjectName("Class1Grade7Interface")
        self.resize(300, 200)  # 设置窗口的初始大小
        self.center_screen()

    def center_screen(self):
        # 获取屏幕尺寸
        app = QApplication.instance()
        screen = app.primaryScreen().availableGeometry()
        # 计算窗口应放置的位置以居中
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2

        # 设置窗口的位置
        self.move(x, y)

    def setup_ui(self):

        self.vBoxLayout = QVBoxLayout(self)
        self.tableView = TableWidget(self)

        self.btnAdd = PushButton("添加")
        self.btnAdd.setMaximumWidth(150)
        self.btnDel = PushButton("删除")
        self.btnDel.setMaximumWidth(150)
        self.btnShare = PushButton("分享")
        self.btnShare.setMaximumWidth(150)
        self.hBoxLayout = QHBoxLayout()

        self.hBoxLayout.addWidget(self.btnAdd)
        self.hBoxLayout.addWidget(self.btnDel)
        self.hBoxLayout.addWidget(self.btnShare)
        # 在最后一个按钮后面添加一个伸展项，使其最右边间距自适应
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hBoxLayout.addSpacerItem(spacer)
        self.vBoxLayout.addLayout(self.hBoxLayout)

        # enable border
        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)

        self.tableView.setWordWrap(False)
        self.tableView.setRowCount(9)
        self.tableView.setColumnCount(6)

        if not QSqlDatabase.contains("qt_sql_default_connection"):
            db = QSqlDatabase.addDatabase("QSQLITE", "qt_sql_default_connection")
            db.setDatabaseName("ClassSchedules.db")
            if not db.open():
                print("Failed to connect to database")
                return
        else:
            db = QSqlDatabase.database("qt_sql_default_connection")

        classInfos = []
        for i in range(1, 10):
            classInfo = ["第 {} 节".format(i)]  # 添加节次信息
            query = QSqlQuery()
            query.prepare("SELECT * FROM C1G7 WHERE ROWID = :rowid")
            query.bindValue(":rowid", i)
            if query.exec() and query.next():
                for j in range(0, 5):
                    classInfo.append(query.value(j))
                classInfos.append(classInfo)
            else:
                print("Failed to fetch data for ROWID:", i)

        for i, classInfo in enumerate(classInfos):
            for j in range(6):
                self.tableView.setItem(i, j, QTableWidgetItem(classInfo[j]))

        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(
            ["节次", "星期一", "星期二", "星期三", "星期四", "星期五"]
        )
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.setStyleSheet("Class1Grade7Interface{background: rgb(255, 255, 255)} ")
        self.vBoxLayout.addWidget(self.tableView)

    def stu_add(self):
        query = QSqlQuery()
        query.prepare("insert into FROM C1G7 WHERE ROWID = :rowid")
        query.addBindValue(":rowid", "")

        if not query.exec():
            QMessageBox.critical(None, "Database Error", query.lastError().text())
            return False

        return True

    def stu_del(self):
        pass

    def stu_modify(self):
        pass

    def stu_query(self):
        pass
