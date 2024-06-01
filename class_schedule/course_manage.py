from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidgetItem,
    QHeaderView,
)
from qfluentwidgets import TableWidget

from common.models import CourseInfo


class CourseManage(QWidget):
    def init_window(self):
        self.setObjectName("CourseManage")
        self.setStyleSheet("CourseManage{background: rgb(255, 255, 255)} ")

    def init_ui(self):
        # 表格
        self.tableView = TableWidget(self)
        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)
        self.tableView.setWordWrap(False)
        self.tableView.setRowCount(9)
        self.tableView.setColumnCount(6)
        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(
            ["节次", "星期一", "星期二", "星期三", "星期四", "星期五"]
        )
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 水平布局
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.tableView)

    def init_data(self):
        course_list = CourseInfo.course_page(1, 10)
        print(course_list)

        field_names = CourseInfo.table_fields()
        for i, classInfo in enumerate(course_list):
            if i == 1:
                data = "第 {} 节".format(i)
                self.tableView.setItem(i, 0, QTableWidgetItem(data))
            else:
                for j in range(1, len(field_names)):
                    data = course_list[i].get(field_names[j])
                    self.tableView.setItem(i, j, QTableWidgetItem(data))

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_window()
        self.init_ui()
        self.init_data()
