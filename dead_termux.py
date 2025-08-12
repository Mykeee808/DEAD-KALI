import sqlite3
import os
import time
import hashlib
import pyfiglet
from rich.console import Console
from rich.table import Table
from rich.progress import track
import random
import string
import sys

console = Console()

# ========================
# Banco de Dados
# ========================
def create_db():
    conn = sqlite3.connect('deadtermux.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, note TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, action TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect('deadtermux.db')
    c = conn.cursor()
    hashed_pass = hashlib.sha256(password.encode()).hexdigest()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pass))
    conn.commit()
    conn.close()

def check_login(username, password):
    conn = sqlite3.connect('deadtermux.db')
    c = conn.cursor()
    hashed_pass = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_pass))
    user = c.fetchone()
    conn.close()
    return user

def add_log(user, action):
    conn = sqlite3.connect('deadtermux.db')
    c = conn.cursor()
    c.execute("INSERT INTO logs (user, action, timestamp) VALUES (?, ?, datetime('now'))", (user, action))
    conn.commit()
    conn.close()

# ========================
# Efeitos Visuais
# ========================
def loading_bar(msg):
    for _ in track(range(20), description=f"[bold red]{msg}[/]"):
        time.sleep(0.05)

def show_ascii(text):
    ascii_art = pyfiglet.figlet_format(text)
    console.print(f"[bold green]{ascii_art}[/]")

def typewriter(text, delay=0.05, color="green"):
    for char in text:
        console.print(f"[bold {color}]{char}[/]", end="")
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ========================
# Ferramentas
# ========================
def gerar_senha():
    tamanho = int(console.input("[bold cyan]Tamanho da senha: [/]"))
    chars = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(random.choice(chars) for _ in range(tamanho))
    console.print(f"[bold green]Senha gerada:[/] {senha}")
    return senha

def bloco_de_notas(user):
    console.print("[bold yellow]1 - Adicionar Nota[/]")
    console.print("[bold yellow]2 - Ler Notas[/]")
    opc = console.input("[bold cyan]Escolha: [/]")
    conn = sqlite3.connect('deadtermux.db')
    c = conn.cursor()
    if opc == "1":
        nota = console.input("[bold cyan]Digite a nota: [/]")
        c.execute("INSERT INTO notes (user, note) VALUES (?, ?)", (user, nota))
        conn.commit()
        console.print("[bold green]Nota salva![/]")
    elif opc == "2":
        c.execute("SELECT note FROM notes WHERE user=?", (user,))
        notas = c.fetchall()
        if notas:
            for n in notas:
                console.print(f"[bold yellow]-[/] {n[0]}")
        else:
            console.print("[bold red]Nenhuma nota encontrada.[/]")
    conn.close()

def ver_logs():
    conn = sqlite3.connect('deadtermux.db')
    c = conn.cursor()
    c.execute("SELECT user, action, timestamp FROM logs")
    logs = c.fetchall()
    table = Table(title="[bold red]Logs de Uso[/]")
    table.add_column("Usuário")
    table.add_column("Ação")
    table.add_column("Data/Hora")
    for log in logs:
        table.add_row(log[0], log[1], log[2])
    console.print(table)
    conn.close()

# ========================
# Sistema Principal
# ========================
def main():
    os.system("clear")
    create_db()
    if not check_login("admin", "admin"):
        add_user("admin", "admin")

    show_ascii("DEAD TERMUX")
    typewriter("Bem-vindo ao inferno digital...", 0.07, "red")

    # Login
    user = None
    while not user:
        username = console.input("[bold green]Usuário: [/]")
        password = console.input("[bold green]Senha: [/]", password=True)
        if check_login(username, password):
            user = username
            add_log(user, "Login realizado")
            loading_bar("Acessando DEAD TERMUX...")
        else:
            typewriter("Acesso Negado ❌", 0.05, "red")

    # Menu
    while True:
        os.system("clear")
        show_ascii("DEAD TERMUX")
        console.print("[bold red]1 - Gerar Senha[/]")
        console.print("[bold red]2 - Bloco de Notas[/]")
        console.print("[bold red]3 - Ver Logs[/]")
        console.print("[bold red]0 - Sair[/]")
        opc = console.input("[bold green]Escolha: [/]")
        if opc == "1":
            add_log(user, "Gerou senha")
            gerar_senha()
        elif opc == "2":
            add_log(user, "Usou bloco de notas")
            bloco_de_notas(user)
        elif opc == "3":
            ver_logs()
        elif opc == "0":
            add_log(user, "Saiu do sistema")
            break
        input("\n[bold cyan]Pressione ENTER para continuar...[/]")

if __name__ == "__main__":
    main()
def check_or_create_login(username, password):
    conn = sqlite3.connect('deadtermux.db')
    c = conn.cursor()
    hashed_pass = hashlib.sha256(password.encode()).hexdigest()
    # Tenta encontrar usuário
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    if user:
        # Usuário existe, confere senha
        if user[2] == hashed_pass:
            conn.close()
            return True
        else:
            conn.close()
            return False
    else:
        # Usuário não existe, cadastra
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pass))
        conn.commit()
        conn.close()
        return True
