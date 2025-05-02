# import sys
# from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Текстовая область")
#         self.setGeometry(100, 100, 400, 300)

#         self.text_edit = QTextEdit(self)
#         self.text_edit.move(50,50)
        

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())


#2 
# import sys
# from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QCheckBox

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Чекбокс")
#         self.setGeometry(100, 100, 300, 200)

#         self.checkbox = QCheckBox("Я согласен", self)
#         self.checkbox.move(50,50)

#         self.label = QLabel("", self)
#         self.label.move(50, 100)
        

#         self.checkbox.stateChanged.connect(self.checkbox_changed)

#     def checkbox_changed(self,state):
#         if state == 2:
#            self.label.setText("Вы согласились!")
#         else:
#             self.label.setText("Вы не согласились! ")
#         self.label.adjustSize()

    
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())

#3 
# import sys
# from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QRadioButton
# from PyQt6.QtGui import QIcon

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("РадиоКнопки")
#         self.setGeometry(100, 100, 300, 200)

#         self.setWindowIcon(QIcon("icon.ico"))

#         self.radio1 = QRadioButton("Вариант 1", self)
#         self.radio1.move(50, 50)
#         self.radio2 = QRadioButton("Вариант 2", self)
#         self.radio2.move(50,80)

#         self.label = QLabel("", self)
#         self.label.move(50, 120)

#         self.radio1.toggled.connect(self.radio_changed)
#         self.radio2.toggled.connect(self.radio_changed)

#     def radio_changed(self):
#         if self.radio1.isChecked():
#             self.label.setText("Выбран Вариант 1")
#         elif self.radio2.isChecked():
#             self.label.setText("Выбран Вариант 2")
#         self.label.adjustSize()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main = MainWindow()
#     main.show()
#     sys.exit(app.exec())


#4 

# import sys
# from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTabWidget


# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Вкладки")
#         self.setGeometry(100, 100, 400, 300)

#         layout = QVBoxLayout()
#         tabs = QTabWidget()

#         tab1 = QWidget()
#         tab1_layout = QVBoxLayout()
#         tab1_layout.addWidget(QLabel("Это первая вкладка"))
#         tab1.setLayout(tab1_layout)

#         tab2 = QWidget()
#         tab2_layout = QVBoxLayout()
#         tab2_layout.addWidget(QLabel("Это вторая вкладка"))
#         tab2.setLayout(tab2_layout)

#         tab3 = QWidget()
#         tab3_layout = QVBoxLayout()
#         tab3_layout.addWidget(QLabel("Это третья вкладка"))
#         tab3.setLayout(tab3_layout)

#         tabs.addTab(tab1, "Вкладка 1")
#         tabs.addTab(tab2, "Вкладка 2")
#         tabs.addTab(tab3, "Вкладка 3")

#         layout.addWidget(tabs)
#         self.setLayout(layout)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())
#5
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QComboBox

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ComboBox пример")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.combo = QComboBox()
        self.combo.addItems(["Python", "Java", "C++", "JavaScript", "Go", "TypeScript"])

        self.label = QLabel("Choose Language")

        self.combo.currentTextChanged.connect(self.language_changed)

        layout.addWidget(self.combo)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def language_changed(self,text):
            self.label.setText(f"You chose: {text}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())