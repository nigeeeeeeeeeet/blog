import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'blog.db')


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            photo TEXT NOT NULL,
            short_description TEXT NOT NULL,
            full_description TEXT NOT NULL
        )
    ''')
    conn.commit()

    row = conn.execute('SELECT COUNT(*) AS cnt FROM users').fetchone()
    if row['cnt'] == 0:
        conn.execute(
            'INSERT INTO users (name, photo, short_description, full_description) '
            'VALUES (?, ?, ?, ?)',
            (
                'jdk',
                'avatar.jpg',
                'Розробник і любитель ігор.',
                'Привіт! Мене звати jdk. Я вивчаю програмування, працюю над '
                'проєктами на Flask і FastAPI, цікавлюся геймдевом та '
                'веброзробкою. У вільний час експериментую з новими '
                'технологіями та створюю власні застосунки.',
            ),
        )
        conn.commit()
    conn.close()


def get_user():
    conn = get_connection()
    user = conn.execute('SELECT * FROM users ORDER BY id LIMIT 1').fetchone()
    conn.close()
    if user is None:
        return None
    return dict(user)


init_db()
