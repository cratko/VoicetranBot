import sqlite3

from database.connect import connect_db


def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    # Создаем таблицу stats
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER,
                       date DATE)''')
    conn.commit()

    # Создаем таблицу users
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER,
                       role TEXT,
                       balance REAL,
                       UNIQUE(user_id))''')  # Используем user_id вместо users_id
    conn.commit()

    conn.close()
