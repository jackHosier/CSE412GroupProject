import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='Pokemon',
                            user='dummy',
                            password='3023')
    return conn


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pokemon;')
    poke = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', poke=poke)

@app.route('/my-link/', methods=['GET', 'POST'])
def my_link():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM move;')
    poke = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', poke=poke)

@app.route('/pokemon-specific/', methods=['POST'])
def pokemon_specific():
    name = request.form['name']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pokemon WHERE pokemon.p_name = %s', (name,))
    poke = cur.fetchone()
    cur.close()
    conn.close()
    if poke is None:
        return render_template('fail.html', searched=name)
    return render_template('poke.html', poke=poke)
