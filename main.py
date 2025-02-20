import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton
from UI.main_window import Ui_MainWindow
from add_edit_form import AddEditCoffeeForm


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.load_data()

        # Подключаем кнопки
        self.ui.addButton.clicked.connect(self.add_record)
        self.ui.editButton.clicked.connect(self.edit_record)

    def load_data(self):
        connection = sqlite3.connect("data/coffee.sqlite")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()

        self.ui.tableWidget.setRowCount(len(rows))
        self.ui.tableWidget.setColumnCount(7)
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Название", "Обжарка", "Молотый", "Описание", "Цена", "Объем"]
        )

        for row_index, row in enumerate(rows):
            for col_index, cell in enumerate(row):
                self.ui.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(cell)))

        connection.close()

    def add_record(self):
        self.form = AddEditCoffeeForm()
        self.form.show()
        self.form.saved.connect(self.load_data)

    def edit_record(self):
        selected = self.ui.tableWidget.currentRow()
        if selected == -1:
            return

        coffee_id = int(self.ui.tableWidget.item(selected, 0).text())
        self.form = AddEditCoffeeForm(coffee_id)
        self.form.show()
        self.form.saved.connect(self.load_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
