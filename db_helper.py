import sqlite3
from sqlite3 import Error

class DBHelper:
    def __init__(self, db_path='db_helperAR.db'):
        self.db_path = db_path
        self._initialize_db()

    def _connect(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON;")
            return conn
        except Error as e:
            print(f"Ошибка подключения к БД: {e}")
            raise

    def _initialize_db(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            name   TEXT    NOT NULL,
            age    INTEGER,
            email  TEXT    UNIQUE
        );
        """
        conn = self._connect()
        try:
            conn.execute(sql)
            conn.commit()
        finally:
            conn.close()
        # conn = self._connect()
        # cursor = conn.cursor()
        # try:
        #     cursor.execute("ALTER TABLE users ADD COLUMN skills TEXT")
        #     conn.commit()
        # finally:  
        #     conn.close()

    def add_user(self, name, age, email=None, skills=None):
        sql = "INSERT INTO users (name, age, email, skills) VALUES (?, ?, ?, ?)"
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(sql, (name, age, email, skills))
            conn.commit()
            return cur.lastrowid
        except Error as e:
            print(f"Ошибка при добавлении пользователя: {e}")
            raise
        finally:
            conn.close()

    def get_all_users(self):
        sql = "SELECT * FROM users ORDER BY id"
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(sql)
            return cur.fetchall()
        finally:
            conn.close()

    def find_users(self, keyword):
        sql = "SELECT * FROM users WHERE name LIKE ? OR email LIKE ?  OR skills LIKE?"
        like = f"%{keyword}%"
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(sql, (like, like, like))
            return cur.fetchall()
        finally:
            conn.close()

    def update_user(self, user_id, name=None, age=None, email=None, skills=None):
        fields = []
        params = []
        if name is not None:
            fields.append("name = ?");   params.append(name)
        if age is not None:
            fields.append("age = ?");    params.append(age)
        if email is not None:
            fields.append("email = ?");  params.append(email)
        if skills is not None:
            fields.append("skills=?"); params.append(skills)

        if not fields:
            return 0
        params.append(user_id)
        sql = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
            return cur.rowcount
        finally:
            conn.close()
    

    def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE id = ?"
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(sql, (user_id,))
            conn.commit()
            return cur.rowcount
        finally:
            conn.close()

    def get_stats(self):
        sql = """ SELECT
        COUNT(*) AS total_users,
        ROUND(AVG(age), 1) AS avg_age,
        COUNT(DISTINCT email) AS unique_emails FROM users"""
        conn = self._connect()
        try:
           cur = conn.cursor()
           cur.execute(sql)
           stats = dict(cur.fetchone())
           
           cur.execute("SELECT skills FROM users WHERE skills IS NOT NULL AND skills != ''")
           skills_rows = cur.fetchall()

           unique_skills = set()
           for row in skills_rows:
               skills = row["skills"]
               skill_list = [s.strip() for s in skills.split(",") if s.strip()]
               unique_skills.update(skill_list)

           stats["unique_skills"] = len(unique_skills)
           return stats
        finally:
             conn.close()