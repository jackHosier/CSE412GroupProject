import os
import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='Pokemon',
                            user='dummy',
                            password='3023')
    return conn

#this is for getting text from the textbox 
@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods =['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text

#for the button 
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    query = my_form_post() #return the string in the text box to this str variable here 

    cur.execute(query)
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

