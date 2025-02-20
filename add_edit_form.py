import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import pyqtSignal


class AddEditCoffeeForm(QDialog):
    saved = pyqtSignal()  # Сигнал для обновления таблицы в главном окне

    def __init__(self, coffee_id=None):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.coffee_id = coffee_id

        if coffee_id:
            self.load_data()

        self.saveButton.clicked.connect(self.save_data)

    def load_data(self):
        """Загружает данные записи для редактирования."""
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM coffee WHERE id=?", (self.coffee_id,))
        row = cursor.fetchone()
        connection.close()

        if row:
            self.nameEdit.setText(row[1])
            self.roastEdit.setText(row[2])
            self.groundCheck.setChecked(bool(row[3]))
            self.descriptionEdit.setText(row[4])
            self.priceEdit.setText(str(row[5]))
            self.volumeEdit.setText(str(row[6]))

    def save_data(self):
        """Сохраняет новую или измененную запись в базу."""
        name = self.nameEdit.text()
        roast = self.roastEdit.text()
        ground = int(self.groundCheck.isChecked())
        description = self.descriptionEdit.text()
        price = self.priceEdit.text()
        volume = self.volumeEdit.text()

        try:
            price = float(price)
            volume = int(volume)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Цена и объем должны быть числами!")
            return

        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()

        if self.coffee_id:
            cursor.execute("""
                UPDATE coffee SET name=?, roast_level=?, ground=?, description=?, price=?, volume=?
                WHERE id=?
            """, (name, roast, ground, description, price, volume, self.coffee_id))
        else:
            cursor.execute("""
                INSERT INTO coffee (name, roast_level, ground, description, price, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, roast, ground, description, price, volume))

        connection.commit()
        connection.close()
        self.saved.emit()
        self.close()
