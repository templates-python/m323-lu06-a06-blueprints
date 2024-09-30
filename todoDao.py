import sqlite3
from todoItem import TodoItem


class TodoDao:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS todo_items""")
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS todo_items (item_id INTEGER PRIMARY KEY, title TEXT, is_completed BOOLEAN)"""
        )
        self.conn.commit()

    def add_item(self, todo_item):
        self.cursor.execute(
            "INSERT INTO todo_items (title, is_completed) VALUES (?, ?)",
            (todo_item.title, todo_item.is_completed),
        )
        self.conn.commit()

    def get_item(self, item_id):
        self.cursor.execute("SELECT * FROM todo_items WHERE item_id = ?", (item_id,))
        row = self.cursor.fetchone()
        if row:
            return TodoItem(row[0], row[1], row[2])
        return None

    def get_all_items(self):
        self.cursor.execute("SELECT * FROM todo_items")
        rows = self.cursor.fetchall()
        todo_items = [TodoItem(row[0], row[1], row[2]) for row in rows]
        return todo_items

    def update_item(self, todo_item):
        self.cursor.execute(
            "UPDATE todo_items SET title = ?, is_completed = ? WHERE item_id = ?",
            (todo_item.title, todo_item.is_completed, todo_item.item_id),
        )
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def delete_item(self, item_id):
        self.cursor.execute("DELETE FROM todo_items WHERE item_id = ?", (item_id,))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def close(self):
        self.conn.close()
