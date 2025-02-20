import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton
from add_edit_form import AddEditCoffeeForm


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.load_data()

        # Подключаем кнопки
        self.addButton.clicked.connect(self.add_record)
        self.editButton.clicked.connect(self.edit_record)

    def load_data(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Название", "Обжарка", "Молотый", "Описание", "Цена", "Объем"]
        )

        for row_index, row in enumerate(rows):
            for col_index, cell in enumerate(row):
                self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(cell)))

        connection.close()

    def add_record(self):
        """Открывает форму для добавления новой записи."""
        self.form = AddEditCoffeeForm()
        self.form.show()
        self.form.saved.connect(self.load_data)

    def edit_record(self):
        """Открывает форму для редактирования выбранной записи."""
        selected = self.tableWidget.currentRow()
        if selected == -1:
            return

        coffee_id = int(self.tableWidget.item(selected, 0).text())  # ID записи
        self.form = AddEditCoffeeForm(coffee_id)
        self.form.show()
        self.form.saved.connect(self.load_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
