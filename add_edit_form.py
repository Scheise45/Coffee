import sqlite3
from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import pyqtSignal
from UI.add_edit_form import Ui_AddEditCoffeeForm


class AddEditCoffeeForm(QDialog):
    saved = pyqtSignal()

    def __init__(self, coffee_id=None):
        super().__init__()
        self.ui = Ui_AddEditCoffeeForm()
        self.ui.setupUi(self)
        self.coffee_id = coffee_id

        if coffee_id:
            self.load_data()

        self.ui.saveButton.clicked.connect(self.save_data)

    def load_data(self):
        connection = sqlite3.connect("data/coffee.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM coffee WHERE id=?", (self.coffee_id,))
        row = cursor.fetchone()
        connection.close()

        if row:
            self.ui.nameEdit.setText(row[1])
            self.ui.roastEdit.setText(row[2])
            self.ui.groundCheck.setChecked(bool(row[3]))
            self.ui.descriptionEdit.setText(row[4])
            self.ui.priceEdit.setText(str(row[5]))
            self.ui.volumeEdit.setText(str(row[6]))

    def save_data(self):
        name = self.ui.nameEdit.text()
        roast = self.ui.roastEdit.text()
        ground = int(self.ui.groundCheck.isChecked())
        description = self.ui.descriptionEdit.text()
        price = self.ui.priceEdit.text()
        volume = self.ui.volumeEdit.text()

        try:
            price = float(price)
            volume = int(volume)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Цена и объем должны быть числами!")
            return

        connection = sqlite3.connect("data/coffee.sqlite")
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
