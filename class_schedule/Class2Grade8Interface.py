# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidgetItem,
    QHeaderView,
)
from qfluentwidgets import TableWidget
from PySide6.QtSql import QSqlDatabase, QSqlQuery


class Class2Grade8Interface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Class2Grade8Interface")

        self.hBoxLayout = QHBoxLayout(self)
        self.tableView = TableWidget(self)

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
            query.prepare("SELECT * FROM C2G8 WHERE ROWID = :rowid")
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
        self.hBoxLayout.addWidget(self.tableView)
