from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            username TEXT,
            name TEXT,
            phone TEXT,
            telegram_nickname TEXT,
            description TEXT,
            timestamp TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS offers (
            username TEXT,
            name TEXT,
            phone TEXT,
            telegram_nickname TEXT,
            description TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM requests')
    requests = c.fetchall()
    c.execute('SELECT * FROM offers')
    offers = c.fetchall()
    conn.close()
    return render_template('index.html', requests=requests, offers=offers)

@app.route('/add_request', methods=['POST'])
def add_request():
    username = request.form['username']
    name = request.form['name']
    phone = request.form['phone']
    telegram_nickname = request.form['telegram_nickname']
    description = request.form['description']
    timestamp = request.form['timestamp']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO requests (username, name, phone, telegram_nickname, description, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, name, phone, telegram_nickname, description, timestamp))
    conn.commit()
    conn.close()
    return 'Запит додано', 200

@app.route('/add_offer', methods=['POST'])
def add_offer():
    username = request.form['username']
    name = request.form['name']
    phone = request.form['phone']
    telegram_nickname = request.form['telegram_nickname']
    description = request.form['description']
    timestamp = request.form['timestamp']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO offers (username, name, phone, telegram_nickname, description, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, name, phone, telegram_nickname, description, timestamp))
    conn.commit()
    conn.close()
    return 'Пропозицію додано', 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
