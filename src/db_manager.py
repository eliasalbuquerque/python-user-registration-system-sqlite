import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER
            )
        ''')
        self.conn.commit()

    def insert_user(self, name, email, age):
        self.cursor.execute('''
            INSERT INTO users (name, email, age) VALUES (?, ?, ?)
        ''', (name, email, age))
        self.conn.commit()

    def get_user(self, user_id=None, select="*", last=False):
        if user_id is not None:
            self.cursor.execute(f"SELECT {select} FROM users WHERE id = ?", (user_id,))
        elif last:
            select_with_id = "id, name, email, age" if select == "*" else f"id, {select}"
            self.cursor.execute(f"SELECT {select_with_id} FROM users ORDER BY id DESC LIMIT 1")
        else:
            select_with_id = "id, " + select if select != "*" else "*"
            self.cursor.execute(f"SELECT {select_with_id} FROM users")
        return self.cursor.fetchall()
            
    def update_user(self, user_id, name, email, age):
        self.cursor.execute('''
            UPDATE users SET name=?, email=?, age=? WHERE id=?
        ''', (name, email, age, user_id))
        self.conn.commit()

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
