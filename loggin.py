import sqlite3
import hashlib

def create_db():
    conn = sqlite3.connect('deadtermux.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def check_or_create_login(username, password):
    conn = sqlite3.connect('deadtermux.db')
    c = conn.cursor()
    hashed_pass = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    if user:
        if user[2] == hashed_pass:
            conn.close()
            return True
        else:
            conn.close()
            return False
    else:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pass))
        conn.commit()
        conn.close()
        return True

def main():
    create_db()
    while True:
        username = input("Usuário: ")
        password = input("Senha: ")
        if check_or_create_login(username, password):
            print("Login OK!")
            break
        else:
            print("Acesso Negado ❌")

if __name__ == "__main__":
    main()
