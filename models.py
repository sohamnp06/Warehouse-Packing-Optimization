import sqlite3

DB_NAME = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS active_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            weight REAL NOT NULL,
            profit REAL NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS history_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            weight REAL NOT NULL,
            profit REAL NOT NULL,
            added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def add_item(name, weight, profit):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO active_items (name, weight, profit) VALUES (?, ?, ?)', (name, weight, profit))
    c.execute('INSERT INTO history_items (name, weight, profit) VALUES (?, ?, ?)', (name, weight, profit))
    conn.commit()
    conn.close()


def get_active_items():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT name, weight, profit FROM active_items')
    items = [{'name': row[0], 'weight': row[1], 'profit': row[2]} for row in c.fetchall()]
    conn.close()
    return items


def get_history_items():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT name, weight, profit, added_on FROM history_items ORDER BY added_on DESC')
    items = [{'name': row[0], 'weight': row[1], 'profit': row[2], 'added_on': row[3]} for row in c.fetchall()]
    conn.close()
    return items


def clear_active_items():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM active_items')
    conn.commit()
    conn.close()
