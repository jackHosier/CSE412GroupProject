import os
import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='Pokemon',
                            user='dummy',
                            password='3023')
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pokemon;')
    poke = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', poke=poke)

@app.route('/my-link/')
def my_link():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM move;')
    poke = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', poke=poke)
