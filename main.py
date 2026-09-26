import os
import sqlite3
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

app = FastAPI(title="User API")


class UserCreate(BaseModel):
    username: str
    email: str


class User(UserCreate):
    id: int


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db_exists = os.path.exists(DB_PATH)

    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()

    if not db_exists:
        conn.executemany(
            'INSERT INTO users (username, email) VALUES (?, ?)',
            [
                ('alice', 'alice@example.com'),
                ('bob', 'bob@example.com'),
                ('carol', 'carol@example.com'),
            ],
        )
        conn.commit()

    conn.close()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/users", response_model=List[User])
def get_users():
    conn = get_connection()
    rows = conn.execute('SELECT id, username, email FROM users').fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    conn = get_connection()
    row = conn.execute(
        'SELECT id, username, email FROM users WHERE id = ?', (user_id,)
    ).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(row)


@app.post("/create_user", response_model=User)
def create_user(user: UserCreate):
    conn = get_connection()
    cur = conn.execute(
        'INSERT INTO users (username, email) VALUES (?, ?)',
        (user.username, user.email),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return User(id=new_id, username=user.username, email=user.email)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
