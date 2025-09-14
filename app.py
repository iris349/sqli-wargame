from flask import Flask, request, render_template, redirect, send_file
import sqlite3
import os
#import webbrowser

app = Flask(__name__)
DB_PATH = 'database.db'

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
        c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
        c.execute("INSERT INTO users (username, password) VALUES ('guest', 'guest')")
        conn.commit()
        conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 취약한 SQL 쿼리 (SQL 인젝션 가능)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        c.execute(query)
        user = c.fetchone()
        conn.close()
        if user:
            return render_template('welcome.html', username=user[1])
        else:
            error = 'Login failed!'
    return render_template('login.html', error=error)


# DB 다운로드 라우트
@app.route('/download/db')
def download_db():
    return send_file(DB_PATH, as_attachment=True)

# 소스코드 다운로드 라우트
@app.route('/download/source')
def download_source():
    return send_file('app.py', as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
