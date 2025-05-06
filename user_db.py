import sqlite3
class UserDB:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self._initialize_db

    def init_db(db_path="users.db"):
       conn = sqlite3.connect(db_path)
       cur = conn.cursor()
       cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT UNIQUE
        )
    """)
       conn.commit()
       conn.close()

    def add_user(name, age, email, db_path="users.db"):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, age, email) VALUES (?,?,?)", (name, age, email))
        conn.commit()
        conn.close()

    def get_all_users(db_path="users.db"):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT id, name, age, email FROM users")
        rows = cur.fetchall()
        conn.close()
        return rows
       
    def list_users(self):
        self.db.list_users()

    if __name__ == '__main__':
       init_db()

    #    add_user("Kamola", "32", "kamola.nimatulaeva@gmail.com")
    #    add_user("Kamola", "32", "kamolanimatulaeva@gmail.com")
    #    add_user("Katy", "30", "katyholmes@rambler.ru")

       users = get_all_users()
    #    for uid, name, age, email in users:
    #        print(uid, name, age, email)
       print(users)
       