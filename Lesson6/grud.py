from PyQt6.QtWidgets import (
QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QMessageBox, QTextEdit, QInputDialog)

import sys 
import crud_alt

class UserApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('User CRUD PyQt6')
        self.setGeometry(100, 100, 600, 450)

        crud_alt.create_table()

        self.layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.city_input = QLineEdit()

        self.layout.addWidget(QLabel('Имя:'))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(QLabel('Возраст:'))
        self.layout.addWidget(self.age_input)
        self.layout.addWidget(QLabel('Email:'))
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(QLabel('Телефрн:'))
        self.layout.addWidget(self.phone_input)
        self.layout.addWidget(QLabel('Город'))
        self.layout.addWidget(self.city_input)

        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton('Добавить')
        self.update_btn = QPushButton('Обновить по ID')
        self.list_btn = QPushButton('Показать всех')
        self.find_btn = QPushButton('Найти')
        self.delete_btn = QPushButton('Удалить по ID')
        self.update_user_city_btn = QPushButton('Обновить город')

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.list_btn)
        btn_layout.addWidget(self.find_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.update_user_city_btn)

        self.layout.addLayout(btn_layout)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.layout.addWidget(self.output)

        self.setLayout(self.layout)

        self.add_btn.clicked.connect(self.add_user)
        self.update_btn.clicked.connect(self.update_user)
        self.list_btn.clicked.connect(self.show_users)
        self.find_btn.clicked.connect(self.find_user)
        self.delete_btn.clicked.connect(self.delete_user)
        self.update_user_city_btn.clicked.connect(self.update_user_city)
    
    def add_user(self):
        name = self.name_input.text()
        age = self.age_input.text()
        email = self.email_input.text()   
        phone = self.phone_input.text()
        city = self.city_input.text()

        if not name or not age:
            QMessageBox.warning(self, "Ошибка", "Имя и возраст обязательны.")
            return
        try:
            conn = crud_alt.connect_db()
            conn.execute("INSERT INTO users (name, age, email, phone, city) VALUES (?, ?, ?, ?, ?)",
                        (name, age, email, phone, city))
            conn.commit()
            conn.close()
            self.output.append(f"[+] Добавлен:{name}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def update_user(self):
        user_id, ok = QInputDialog.getText(self, "Обновить", "Введите ID пользователя")
        if ok:
            name = self.name_input.text()
            age = self.age_input.text()
            email = self.email_input.text()
            phone = self.phone_input.text()
            city = self.city_input.text()

            if not name or not age:
                QMessageBox.warning(self, "Ошибка", "Имя и возраст обязательны.")
                return
            
            count = crud_alt.update_user(user_id, name, age, email, phone, city)
            if count:
                self.output.append(f"[Обновление] Пользователь ID ={user_id} обновлен")
            
            else:
                self.output.append(f"[!] Пользователь не найден.")

    def update_user_city(self):
        user_id, ok = QInputDialog.getText(self, "Обновить город", "Введите ID пользователя")
        if not ok:
            return
        city, ok = QInputDialog.getText(self, "Обновить город", "Введите новый город")
        if not ok:
            return
        
        count = crud_alt.update_user_city(user_id, city)
        if count:
            self.output.append(f"[Обновление] Город пользователя  ={city} обновлен")
        else:
            self.output.append(f"[!] Пользователь не найден.")




    def show_users(self):
        conn = crud_alt.connect_db()
        users = conn.execute("SELECT * FROM users").fetchall()
        self.output.clear()
        for u in users:
            self.output.append(f"{u[0]} | {u[1]}  | {u[2]}  |  {u[3]}  |  {u[4]} | {u[5]}")
        conn.close()

    def find_user(self):
        keyword, ok = QInputDialog.getText(self, "Поиск", "Введите имя/email/телефон/город:")
        if ok and keyword:
            conn = crud_alt.connect_db()
            sql = "SELECT * FROM users WHERE name LIKE ? OR email LIKE ? OR phone LIKE ? OR city LIKE ?"
            results = conn.execute(sql, [f"%{keyword}%"]  * 4).fetchall()
            conn.close()
            self.output.clear()
            if results:
                for u in results:
                    self.output.append(f"{u[0]} | {u[1]}  | {u[2]}  |  {u[3]}  |  {u[4]} | {u[5]}")
            else:
                self.output.append(f"[!] Ничего не найдено.")

    def delete_user(self):
        user_id, ok = QInputDialog.getText(self, "Удаление", "Введите ID пользователя:")
        if ok:
            confirm = QMessageBox.question(
                self, "Подтвердите", f"Удалить пользователя с ID={user_id}?",
            )
            if confirm == QMessageBox.StandardButton.Yes:
                conn = crud_alt.connect_db()
                cur = conn.execute("DELETE FEOM users WHERE id =?", (user_id,))
                conn.commit()
                if cur.rowcount:
                    self.output.append(f"[-] Удален пользователь ID={user_id} ")
                else:
                   self.output.append(f"[!] Пользователь не найден. ")
                conn.close()

if __name__ == '__main__':
        app = QApplication(sys.argv)
        win = UserApp()
        win.show()
        sys.exit(app.exec())
