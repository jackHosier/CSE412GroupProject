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
    cur.execute('WITH type2(p_name2, t2) AS (SELECT p_name, t_name FROM pokemon, pokemon_type, type WHERE p_poke_id = pt_poke_id AND pt_type_id = t_type_id AND pt_slot = 2), type1(p_name3, t_name) AS (SELECT p_name, t_name FROM pokemon, pokemon_type, type WHERE p_poke_id = pt_poke_id AND pt_type_id = t_type_id AND pt_slot = 1 EXCEPT (SELECT p_name, t_name FROM pokemon, pokemon_type, type, type2 WHERE p_poke_id = pt_poke_id AND pt_type_id = t_type_id AND pt_slot = 1 AND p_name = p_name2)) SELECT p_name3, t_name, NULL, p_poke_id, p_dex, p_height, p_weight FROM type1, pokemon WHERE p_name3 = p_name UNION SELECT p_name, t_name, t2, p_poke_id, p_dex, p_height, p_weight FROM pokemon, pokemon_type, type, type2 WHERE p_poke_id = pt_poke_id AND pt_type_id = t_type_id AND pt_slot = 1 AND p_name = p_name2 ORDER BY p_dex, p_poke_id ASC;')
    poke = cur.fetchall()
    total_list = []
    for pok in poke:
        pok_list = list(pok)
        pok_list[5] = float(pok_list[5])/10
        pok_list[6] = float(pok_list[6])/10
        pok = tuple(pok_list)
        total_list.append(pok)
    cur.close()
    conn.close()
    return render_template('index.html', poke=total_list)

@app.route('/move-list/', methods=['GET', 'POST'])
def move_list():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT m_name, t_name, m_power, m_pp, m_accuracy, m_priority, mdc_name, me_short_effect, m_effect_chance FROM move, type, move_effect_prose, move_damage_class WHERE move.m_type_id = type.t_type_id AND move.m_damage_class_id = mdc_damage_class_id AND move.m_effect_id = me_effect_id;')
    move = cur.fetchall()
    total_list = []
    for mov in move:
        if mov[8] is not None:
            move_list = list(mov)
            move_list[7] = move_list[7].replace("$effect_chance", str(move_list[8]))
            mov = tuple(move_list)
        total_list.append(mov)
    cur.close()
    conn.close()
    return render_template('type_move.html', move=total_list)

@app.route('/pokemon-specific/', methods=['POST'])
def pokemon_specific():
    name = str.lower(request.form['name'])
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pokemon WHERE pokemon.p_name = %s', (name,))
    poke = cur.fetchone()
    cur.close()
    conn.close()
    if poke is None:
        return render_template('fail.html', searched=name)
    return render_template('poke.html', poke=poke)

@app.route('/move-specific/', methods=['POST'])
def move_specific():
    name = str.lower(request.form['name'])
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pokemon WHERE pokemon.p_name = %s', (name,))
    poke = cur.fetchone()
    cur.close()
    conn.close()
    if poke is None:
        return render_template('fail.html', searched=name)
    return render_template('poke.html', poke=poke)

@app.route('/type-move/', methods=['POST'])
def type_move():
    type = str.lower(request.form['type_'])
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT m_name, t_name, m_power, m_pp, m_accuracy, m_priority, mdc_name, me_short_effect, m_effect_chance FROM move, type, move_effect_prose, move_damage_class WHERE move.m_type_id = type.t_type_id AND move.m_damage_class_id = mdc_damage_class_id AND move.m_effect_id = me_effect_id AND type.t_name = %s', (type,))
    move = cur.fetchall()
    total_list = []
    for mov in move:
        if mov[8] is not None:
            move_list = list(mov)
            move_list[7] = move_list[7].replace("$effect_chance", str(move_list[8]))
            mov = tuple(move_list)
        total_list.append(mov)
            
    cur.close()
    conn.close()
    if move is None:
        return render_template('fail.html', searched=type)
    return render_template('type_move.html', move=total_list)

