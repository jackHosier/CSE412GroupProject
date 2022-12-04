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
        if pok[2] is None:
            pok_list = list(pok)
            pok_list[2] = 'None'
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
        if mov[2] is None:
            move_list = list(mov)
            move_list[2] = "—"
            mov = tuple(move_list)
        if mov[4] is None:
            move_list = list(mov)
            move_list[4] = "—"
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

    cur.execute('WITH type2(p_name2, t2) AS (SELECT p_name, t_name FROM pokemon, pokemon_type, type WHERE p_poke_id = pt_poke_id AND pt_type_id = t_type_id AND pt_slot = 2), type1(p_name3, t_name) AS (SELECT p_name, t_name FROM pokemon, pokemon_type, type WHERE p_poke_id = pt_poke_id AND pt_type_id = t_type_id AND pt_slot = 1 EXCEPT (SELECT p_name, t_name FROM pokemon, pokemon_type, type, type2 WHERE p_poke_id = pt_poke_id AND pt_type_id = t_type_id AND pt_slot = 1 AND p_name = p_name2)), dex_id(dex) AS (SELECT p_dex FROM pokemon WHERE p_name LIKE %s) SELECT p_name3, t_name, NULL, p_poke_id, p_dex, p_height, p_weight FROM type1, pokemon, dex_id WHERE p_name3 = p_name AND p_dex = dex UNION SELECT p_name, t_name, t2, p_poke_id, p_dex, p_height, p_weight FROM pokemon, pokemon_type, type, type2, dex_id WHERE p_poke_id = pt_poke_id AND pt_type_id = t_type_id AND pt_slot = 1 AND p_name = p_name2 AND p_dex = dex ORDER BY p_dex, p_poke_id ASC;', ('%'+name+'%',))
    poke = cur.fetchall()
    total_list = []
    for pok in poke:
        pok_list = list(pok)
        pok_list[5] = float(pok_list[5])/10
        pok_list[6] = float(pok_list[6])/10
        pok = tuple(pok_list)
        if pok[2] is None:
            pok_list = list(pok)
            pok_list[2] = 'None'
            pok = tuple(pok_list)
        total_list.append(pok)

    cur.execute('WITH dex_id(dex) AS (SELECT p_dex FROM pokemon WHERE p_name LIKE %s) SELECT p_name, m_name, t_name, m_power, m_pp, m_accuracy, m_priority, mdc_name, me_short_effect, m_effect_chance, mm_name, pm_level FROM pokemon, pokemon_move, move_method, move, type, move_damage_class, move_effect_prose, dex_id WHERE p_poke_id = pm_poke_id AND pm_move_id = m_move_id AND pm_move_method_id = mm_move_method_id AND m_type_id = t_type_id AND m_damage_class_id = mdc_damage_class_id AND me_effect_id = m_effect_id AND pm_version_group_id = 20 AND p_dex = dex ORDER BY p_name, mm_name, pm_level ASC;', ('%'+name+'%',))
    moves = cur.fetchall()
    total_list2 = []
    for mov in moves:
        if mov[8] is not None:
            move_list = list(mov)
            move_list[7] = move_list[7].replace("$effect_chance", str(move_list[8]))
            mov = tuple(move_list)
        if mov[2] is None:
            move_list = list(mov)
            move_list[2] = "—"
            mov = tuple(move_list)
        if mov[4] is None:
            move_list = list(mov)
            move_list[4] = "—"
            mov = tuple(move_list)
        total_list2.append(mov)

    cur.execute('WITH chain_id(evo_chain) AS (SELECT ps_evolution_chain_id FROM pokemon, pokemon_species, pokemon_evolution WHERE p_poke_id = ps_evolves_from_species_id AND pe_evolved_species_id = ps_poke_id AND (ps_name LIKE %s OR p_name LIKE %s)) (SELECT DISTINCT p_poke_id, pe_evolved_species_id, p_name, ps_name, et_identifier, pe_minimum_level, pe_minimum_happiness,pe_gender_id, NULL AS item,pe_time_of_day,NULL AS kmove,NULL AS ktmove, COUNT(pe_location_id) AS loc FROM pokemon, pokemon_species, pokemon_evolution, chain_id, evolution_trigger WHERE p_poke_id = ps_evolves_from_species_id AND pe_evolved_species_id = ps_poke_id AND ps_evolution_chain_id = evo_chain AND et_evolution_trigger = pe_evolution_trigger_id GROUP BY p_poke_id, pe_evolved_species_id, p_name, ps_name, et_identifier, pe_minimum_level, pe_minimum_happiness, pe_gender_id, pe_time_of_day HAVING COUNT(pe_trigger_item_id) = 0 AND COUNT(pe_held_item_id) = 0 AND COUNT(pe_known_move_id) = 0 AND COUNT(pe_known_move_type_id) = 0 UNION SELECT DISTINCT p_poke_id, pe_evolved_species_id, p_name, ps_name, et_identifier, pe_minimum_level, pe_minimum_happiness,pe_gender_id,i_name AS item,pe_time_of_day,NULL AS kmove,NULL AS ktmove, COUNT(pe_location_id) AS loc FROM pokemon, pokemon_species, pokemon_evolution, chain_id, evolution_trigger, item WHERE p_poke_id = ps_evolves_from_species_id AND pe_evolved_species_id = ps_poke_id AND ps_evolution_chain_id = evo_chain AND et_evolution_trigger = pe_evolution_trigger_id AND (i_item_id = pe_trigger_item_id OR i_item_id = pe_held_item_id) GROUP BY p_poke_id, pe_evolved_species_id, p_name, ps_name, et_identifier, pe_minimum_level, pe_minimum_happiness, pe_gender_id, pe_time_of_day, i_name UNION SELECT DISTINCT p_poke_id, pe_evolved_species_id, p_name, ps_name, et_identifier, pe_minimum_level, pe_minimum_happiness,pe_gender_id, NULL AS item,pe_time_of_day,m_name AS kmove,NULL AS ktmove, COUNT(pe_location_id) AS loc FROM pokemon, pokemon_species, pokemon_evolution, chain_id, evolution_trigger, move WHERE p_poke_id = ps_evolves_from_species_id AND pe_evolved_species_id = ps_poke_id AND ps_evolution_chain_id = evo_chain AND et_evolution_trigger = pe_evolution_trigger_id AND pe_known_move_id = m_move_id GROUP BY p_poke_id, pe_evolved_species_id, p_name, ps_name, et_identifier, pe_minimum_level, pe_minimum_happiness, pe_gender_id, pe_time_of_day, m_name UNION SELECT DISTINCT p_poke_id, pe_evolved_species_id, p_name, ps_name, et_identifier, pe_minimum_level, pe_minimum_happiness,pe_gender_id, NULL AS item,pe_time_of_day,NULL AS kmove,t_name AS ktmove, COUNT(pe_location_id) AS loc FROM pokemon, pokemon_species, pokemon_evolution, chain_id, evolution_trigger, type WHERE p_poke_id = ps_evolves_from_species_id AND pe_evolved_species_id = ps_poke_id AND ps_evolution_chain_id = evo_chain AND et_evolution_trigger = pe_evolution_trigger_id AND pe_known_move_type_id = t_type_id GROUP BY p_poke_id, pe_evolved_species_id, p_name, ps_name, et_identifier, pe_minimum_level, pe_minimum_happiness, pe_gender_id, pe_time_of_day, t_name) ORDER BY p_poke_id, pe_evolved_species_id, ps_name', ('%' + name + '%','%' + name + '%',))
    evol = cur.fetchall()
    total_list3 = []
    for evo in evol:
        if evo[12] > 0:
            evo_list = list(evo)
            evo_list[12] = 'True'
            evo = tuple(evo_list)
        if evo[12] == 0:
            evo_list = list(evo)
            evo_list[12] = 'False'
            evo = tuple(evo_list)
        if evo[7] == 1:
            evo_list = list(evo)
            evo_list[7] = 'Female'
            evo = tuple(evo_list)
        if evo[7] == 2:
            evo_list = list(evo)
            evo_list[7] = 'Male'
            evo = tuple(evo_list)
        total_list3.append(evo)

    cur.execute('WITH dex_id(dex) AS (SELECT p_dex FROM pokemon WHERE p_name LIKE %s), type1(pname, tname, df1) AS (SELECT p_name, t_name, te_damage_factor FROM pokemon, pokemon_type, type, type_effective, dex_id WHERE pt_poke_id = p_poke_id AND p_dex = dex AND te_target_type_id = pt_type_id AND t_type_id = te_damage_type_id AND pt_slot = 1), type2(pname, tname, df2) AS (SELECT p_name, t_name, te_damage_factor FROM pokemon, pokemon_type, type, type_effective, dex_id WHERE pt_poke_id = p_poke_id AND p_dex = dex AND te_target_type_id = pt_type_id AND t_type_id = te_damage_type_id AND pt_slot = 2) SELECT type1.pname, type1.tname, (df1 * df2)/100 FROM type1, type2 WHERE type1.tname = type2.tname UNION (SELECT pname, tname, df1 FROM type1 EXCEPT SELECT type1.pname, type1.tname, df1 FROM type1, type2 WHERE type1.tname = type2.tname) ORDER BY pname, tname ASC', ('%'+name+'%',))
    damage = cur.fetchall()

    cur.close()
    conn.close()

    if total_list == []:
        return render_template('fail.html', searched=name)
    if total_list2 == []:
        return render_template('fail.html', searched=name)
    
    return render_template('poke.html', poke=total_list, move=total_list2, evo=total_list3, damage=damage)

@app.route('/move-specific/', methods=['POST'])
def move_specific():
    input = str.lower(request.form['move'])
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT m_name, t_name, m_power, m_pp, m_accuracy, m_priority, mdc_name, me_short_effect, m_effect_chance FROM move, type, move_effect_prose, move_damage_class WHERE move.m_type_id = type.t_type_id AND move.m_damage_class_id = mdc_damage_class_id AND move.m_effect_id = me_effect_id AND move.m_name = %s', (input,))
    moves = cur.fetchall()
    total_list = []
    for mov in moves:
        if mov[8] is not None:
            move_list = list(mov)
            move_list[7] = move_list[7].replace("$effect_chance", str(move_list[8]))
            mov = tuple(move_list)
        if mov[2] is None:
            move_list = list(mov)
            move_list[2] = "—"
            mov = tuple(move_list)
        if mov[4] is None:
            move_list = list(mov)
            move_list[4] = "—"
            mov = tuple(move_list)
        total_list.append(mov)

    cur.execute('WITH type2(p_name2, t2) AS (SELECT p_name, t_name FROM pokemon, pokemon_type, type WHERE p_poke_id = pt_poke_id AND pt_type_id = t_type_id AND pt_slot = 2), type1(p_name3, t_name) AS (SELECT p_name, t_name FROM pokemon, pokemon_type, type WHERE p_poke_id = pt_poke_id AND pt_type_id = t_type_id AND pt_slot = 1 EXCEPT (SELECT p_name, t_name FROM pokemon, pokemon_type, type, type2 WHERE p_poke_id = pt_poke_id AND pt_type_id = t_type_id AND pt_slot = 1 AND p_name = p_name2)), ptypes(p_name, t1, t2, p_id, p_dex, p_height, p_weight) AS (SELECT p_name3, t_name, NULL, p_poke_id, p_dex, p_height, p_weight FROM type1, pokemon WHERE p_name3 = p_name UNION SELECT p_name, t_name, t2, p_poke_id, p_dex, p_height, p_weight FROM pokemon, pokemon_type, type, type2 WHERE p_poke_id = pt_poke_id AND pt_type_id = t_type_id AND pt_slot = 1 AND p_name = p_name2 ORDER BY p_dex, p_poke_id ASC)SELECT DISTINCT p_name, t1, t2, p_id, p_dex, p_height, p_weight, mm_name, pm_level FROM ptypes, pokemon_move, move, move_method WHERE p_id=pm_poke_id AND pm_move_id = m_move_id AND pm_move_method_id = mm_move_method_id AND pm_version_group_id = 20 AND m_name = %s ORDER BY p_dex, p_id ASC', (input,))
    poke = cur.fetchall()
    total_list2 = []
    for pok in poke:
        pok_list = list(pok)
        pok_list[5] = float(pok_list[5])/10
        pok_list[6] = float(pok_list[6])/10
        pok = tuple(pok_list)
        if pok[2] is None:
            pok_list = list(pok)
            pok_list[2] = 'None'
            pok = tuple(pok_list)
        total_list2.append(pok)
    
    cur.close()
    conn.close()

    if total_list == []:
        return render_template('fail.html', searched=input)
    if total_list2 == []:
        return render_template('fail.html', searched=input)
    return render_template('move.html', poke=total_list2, move=total_list)

@app.route('/type/', methods=['POST'])
def type():
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
        if mov[2] is None:
            move_list = list(mov)
            move_list[2] = "—"
            mov = tuple(move_list)
        if mov[4] is None:
            move_list = list(mov)
            move_list[4] = "—"
            mov = tuple(move_list)
        total_list.append(mov)
    
    cur.execute('WITH type2(p_name2, t2) AS (SELECT p_name, t_name FROM pokemon, pokemon_type, type WHERE p_poke_id = pt_poke_id AND pt_type_id = t_type_id AND pt_slot = 2), type1(p_name3, t_name) AS (SELECT p_name, t_name FROM pokemon, pokemon_type, type WHERE p_poke_id = pt_poke_id AND pt_type_id = t_type_id AND pt_slot = 1 EXCEPT (SELECT p_name, t_name FROM pokemon, pokemon_type, type, type2 WHERE p_poke_id = pt_poke_id AND pt_type_id = t_type_id AND pt_slot = 1 AND p_name = p_name2)), ptypes(p_name, t1, t2, p_id, p_dex, p_height, p_weight) AS (SELECT p_name3, t_name, NULL, p_poke_id, p_dex, p_height, p_weight FROM type1, pokemon WHERE p_name3 = p_name UNION SELECT p_name, t_name, t2, p_poke_id, p_dex, p_height, p_weight FROM pokemon, pokemon_type, type, type2 WHERE p_poke_id = pt_poke_id AND pt_type_id = t_type_id AND pt_slot = 1 AND p_name = p_name2 ORDER BY p_dex, p_poke_id ASC) SELECT * FROM ptypes WHERE t1 = %s OR t2 = %s', (type,type,))
    poke = cur.fetchall()
    total_list2 = []
    for pok in poke:
        pok_list = list(pok)
        pok_list[5] = float(pok_list[5])/10
        pok_list[6] = float(pok_list[6])/10
        pok = tuple(pok_list)
        if pok[2] is None:
            pok_list = list(pok)
            pok_list[2] = 'None'
            pok = tuple(pok_list)
        total_list2.append(pok)
    cur.close()
    conn.close()
    if total_list == []:
        return render_template('fail.html', searched=type)
    if total_list2 == []:
        return render_template('fail.html', searched=type)
    return render_template('type.html', poke=total_list2, move=total_list)

