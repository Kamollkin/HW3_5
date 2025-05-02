import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton,QLineEdit, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Задача")
        self.setGeometry(200, 200, 300, 150)

        self.label = QLabel("Сколько будет 2+3?" ,self)
        self.line_edit = QLineEdit(self)
        self.button = QPushButton("Проверить", self)
        self.button.clicked.connect(self.change_label)
        

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def change_label(self):
        answer = self.line_edit.text()
        if  answer == "5":
            self.label.setText("Правильно!")
        else:
            self.label.setText("Неправильно!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())