import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.load_data()

    def load_data(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()

        # Получаем данные
        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()

        # Заполняем таблицу
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Название", "Обжарка", "Молотый", "Описание", "Цена", "Объем"])

        for row_index, row in enumerate(rows):
            for col_index, cell in enumerate(row):
                self.tableWidget.setItem(
                    row_index, col_index, QTableWidgetItem(str(cell)))

        connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
