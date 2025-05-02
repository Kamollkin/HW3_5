
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QCheckBox, QPushButton, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Напитки")
        self.setGeometry(200, 200, 400, 300)

        self.coffee_checkbox = QCheckBox("Кофе")
        self.tea_checkbox = QCheckBox("Чай")
        self.juice_checkbox = QCheckBox("Сок")

        self.button = QPushButton("Показать выбор:")
        self.button.clicked.connect(self.show_selection)

        self.label = QLabel("")


        layout = QVBoxLayout()
        layout.addWidget(self.coffee_checkbox)
        layout.addWidget(self.tea_checkbox)
        layout.addWidget(self.juice_checkbox)
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        self.setLayout(layout)


    def show_selection(self):
        selected = []
        if self.coffee_checkbox.isChecked():
            selected.append("Кофе")
        if self.tea_checkbox.isChecked():
            selected.append("Чай")
        if self.juice_checkbox.isChecked():
            selected.append("Сок")

        self.label.setText(", ".join(selected))
    

        self.label.adjustSize()

    
if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   sys.exit(app.exec())
        