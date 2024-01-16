import sqlite3
import threading

class DatabaseManager(object):

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.lock = threading.Lock()

        self.create_tables()

    def create_tables(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT,datecreate TIMESTAMP DEFAULT CURRENT_TIMESTAMP, datechange TIMESTAMP DEFAULT CURRENT_TIMESTAMP, title TEXT,text TEXT, color TEXT DEFAULT [#E8E9E4])')

    def save_to_database(self, value, noteid):
        with self.lock:
            self.cursor.execute("UPDATE products SET `text` = ?, `title` = ? WHERE id = ?", (value,value.splitlines()[0], noteid))
            return self.connection.commit()

    def create_new_note(self):
        self.cursor.execute("INSERT INTO products DEFAULT VALUES")
        self.connection.commit()
        newnote = self.cursor.execute("SELECT * FROM products ORDER BY datecreate DESC LIMIT 2")
        return newnote.fetchone()

    def get_all_notes(self):
        self.cursor.execute("SELECT * FROM products ORDER BY datechange DESC")
        rows = self.cursor.fetchall()
        return rows

    def click_note(self, noteid):
        noteid = (noteid,)
        note = self.cursor.execute("SELECT * FROM products ORDER BY datecreate DESC LIMIT 1 OFFSET ?", (noteid))
        return note.fetchone()

    def delete_note(self, noteid):
        noteid = (noteid,)
        self.cursor.execute("DELETE FROM products WHERE id = ?", (noteid))
        self.connection.commit()

    def save_text_color(self, color, noteid):
        with self.lock:
            self.cursor.execute("UPDATE products SET `color` = ? WHERE id = ?", (color, noteid))
            return self.connection.commit()


