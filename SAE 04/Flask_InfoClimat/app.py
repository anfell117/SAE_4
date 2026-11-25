#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, flash
from flask import session, g
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="serveurmysql.iut-bm.univ-fcomte.fr",   # à modifier
            user="aderardj",                             # à modifier
            password="secret",                           # à modifier
            database="BDD_aderardj",                     # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# ============== ANIMATEUR ==============
@app.route('/')
@app.route('/animateur/show')
def show_animateur():
    mycursor = get_db().cursor()
    sql = '''SELECT animateur.id_animateur, animateur.nom_animateur, animateur.prenom_animateur,
    animateur.telephone_animateur, animateur.disponibilite,
    adresse.nom_rue, adresse.numero_rue
    FROM animateur
    JOIN adresse ON animateur.adresse_id = adresse.id_adresse
    ORDER BY animateur.nom_animateur;'''
    mycursor.execute(sql)
    animateurs = mycursor.fetchall()
    return render_template('animateur/show_animateur.html', animateurs=animateurs)


@app.route('/animateur/add', methods=['GET'])
def add_animateur():
    mycursor = get_db().cursor()
    sql = '''SELECT id_adresse, nom_rue, numero_rue FROM adresse ORDER BY nom_rue;'''
    mycursor.execute(sql)
    adresses = mycursor.fetchall()
    return render_template('animateur/add_animateur.html', adresses=adresses)


@app.route('/animateur/add', methods=['POST'])
def valid_add_animateur():
    nom_animateur = request.form.get('nom_animateur')
    prenom_animateur = request.form.get('prenom_animateur')
    telephone_animateur = request.form.get('telephone_animateur')
    disponibilite = 1 if request.form.get('disponibilite') else 0
    adresse_id = request.form.get('adresse_id')
    mycursor = get_db().cursor()
    tuple_param = (nom_animateur, prenom_animateur, telephone_animateur, disponibilite, adresse_id)
    sql = '''INSERT INTO animateur(id_animateur, nom_animateur, prenom_animateur, telephone_animateur, disponibilite, adresse_id)
    VALUES (NULL, %s, %s, %s, %s, %s);'''
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/animateur/show')


@app.route('/animateur/edit', methods=['GET'])
def edit_animateur():
    id = request.args.get('id')
    mycursor = get_db().cursor()
    sql = '''SELECT id_animateur, nom_animateur, prenom_animateur, telephone_animateur, disponibilite, adresse_id
    FROM animateur
    WHERE id_animateur=%s;'''
    mycursor.execute(sql, (id,))
    animateur = mycursor.fetchone()
    sql = '''SELECT id_adresse, nom_rue, numero_rue FROM adresse ORDER BY nom_rue;'''
    mycursor.execute(sql)
    adresses = mycursor.fetchall()
    return render_template('animateur/edit_animateur.html', animateur=animateur, adresses=adresses)


@app.route('/animateur/edit', methods=['POST'])
def valid_edit_animateur():
    id = request.form.get('id')
    nom_animateur = request.form.get('nom_animateur')
    prenom_animateur = request.form.get('prenom_animateur')
    telephone_animateur = request.form.get('telephone_animateur')
    disponibilite = 1 if request.form.get('disponibilite') else 0
    adresse_id = request.form.get('adresse_id')
    mycursor = get_db().cursor()
    tuple_param = (nom_animateur, prenom_animateur, telephone_animateur, disponibilite, adresse_id, id)
    sql = '''UPDATE animateur
    SET nom_animateur = %s, prenom_animateur = %s, telephone_animateur = %s, disponibilite = %s, adresse_id = %s
    WHERE id_animateur=%s;'''
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/animateur/show')


@app.route('/animateur/delete')
def delete_animateur():
    id = request.args.get('id', 0)
    mycursor = get_db().cursor()
    tuple_param = (id,)
    mycursor.execute("DELETE FROM animer WHERE animateur_id=%s;", tuple_param)
    mycursor.execute("DELETE FROM s_occuper WHERE animateur_id=%s;", tuple_param)
    mycursor.execute("DELETE FROM former WHERE animateur_id=%s;", tuple_param)
    mycursor.execute("DELETE FROM travailler WHERE animateur_id=%s;", tuple_param)
    mycursor.execute("DELETE FROM animateur WHERE id_animateur=%s;", tuple_param)
    get_db().commit()
    return redirect('/animateur/show')


# ============== ANIMATION ==============
@app.route('/animation/show')
def show_animation():
    mycursor = get_db().cursor()
    sql = '''SELECT animation.id_animation, animation.nom_animation, animation.nb_places_disponibles,
    animation.date_animation, atelier.nom_atelier, adresse.nom_rue, adresse.numero_rue
    FROM animation
    JOIN atelier ON animation.atelier_id = atelier.id_atelier
    JOIN adresse ON animation.adresse_id = adresse.id_adresse
    ORDER BY animation.date_animation;'''
    mycursor.execute(sql)
    animations = mycursor.fetchall()
    return render_template('animation/show_animation.html', animations=animations)


@app.route('/animation/add', methods=['GET'])
def add_animation():
    mycursor = get_db().cursor()
    sql = '''SELECT id_atelier, nom_atelier FROM atelier ORDER BY nom_atelier;'''
    mycursor.execute(sql)
    ateliers = mycursor.fetchall()
    sql = '''SELECT id_adresse, nom_rue, numero_rue FROM adresse ORDER BY nom_rue;'''
    mycursor.execute(sql)
    adresses = mycursor.fetchall()
    return render_template('animation/add_animation.html', ateliers=ateliers, adresses=adresses)


@app.route('/animation/add', methods=['POST'])
def valid_add_animation():
    nom_animation = request.form.get('nom_animation')
    nb_places_disponibles = request.form.get('nb_places_disponibles')
    date_animation = request.form.get('date_animation')
    atelier_id = request.form.get('atelier_id')
    adresse_id = request.form.get('adresse_id')
    mycursor = get_db().cursor()
    tuple_param = (nom_animation, nb_places_disponibles, date_animation, atelier_id, adresse_id)
    sql = '''INSERT INTO animation(id_animation, nom_animation, nb_places_disponibles, date_animation, atelier_id, adresse_id)
    VALUES (NULL, %s, %s, %s, %s, %s);'''
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/animation/show')


@app.route('/animation/edit', methods=['GET'])
def edit_animation():
    id = request.args.get('id')
    mycursor = get_db().cursor()
    sql = '''SELECT id_animation, nom_animation, nb_places_disponibles, date_animation, atelier_id, adresse_id
    FROM animation
    WHERE id_animation=%s;'''
    mycursor.execute(sql, (id,))
    animation = mycursor.fetchone()
    sql = '''SELECT id_atelier, nom_atelier FROM atelier ORDER BY nom_atelier;'''
    mycursor.execute(sql)
    ateliers = mycursor.fetchall()
    sql = '''SELECT id_adresse, nom_rue, numero_rue FROM adresse ORDER BY nom_rue;'''
    mycursor.execute(sql)
    adresses = mycursor.fetchall()
    return render_template('animation/edit_animation.html', animation=animation, ateliers=ateliers, adresses=adresses)


@app.route('/animation/edit', methods=['POST'])
def valid_edit_animation():
    id = request.form.get('id')
    nom_animation = request.form.get('nom_animation')
    nb_places_disponibles = request.form.get('nb_places_disponibles')
    date_animation = request.form.get('date_animation')
    atelier_id = request.form.get('atelier_id')
    adresse_id = request.form.get('adresse_id')
    mycursor = get_db().cursor()
    tuple_param = (nom_animation, nb_places_disponibles, date_animation, atelier_id, adresse_id, id)
    sql = '''UPDATE animation
    SET nom_animation = %s, nb_places_disponibles = %s, date_animation = %s, atelier_id = %s, adresse_id = %s
    WHERE id_animation=%s;'''
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/animation/show')


@app.route('/animation/delete')
def delete_animation():
    id = request.args.get('id', 0)
    mycursor = get_db().cursor()
    tuple_param = (id,)
    mycursor.execute("DELETE FROM animer WHERE animation_id=%s;", tuple_param)
    mycursor.execute("DELETE FROM participer WHERE animation_id=%s;", tuple_param)
    mycursor.execute("DELETE FROM animation WHERE id_animation=%s;", tuple_param)
    get_db().commit()
    return redirect('/animation/show')


# ============== PARTICIPANT ==============
@app.route('/participant/show')
def show_participant():
    mycursor = get_db().cursor()
    sql = '''SELECT participant.id_participant, participant.prenom_participant, participant.nom_participant,
    participant.adresse_mail_participant, participant.telephone, participant.present,
    adresse.nom_rue, adresse.numero_rue
    FROM participant
    JOIN adresse ON participant.adresse_id = adresse.id_adresse
    ORDER BY participant.nom_participant;'''
    mycursor.execute(sql)
    participants = mycursor.fetchall()
    return render_template('participant/show_participant.html', participants=participants)


@app.route('/participant/add', methods=['GET'])
def add_participant():
    mycursor = get_db().cursor()
    sql = '''SELECT id_adresse, nom_rue, numero_rue FROM adresse ORDER BY nom_rue;'''
    mycursor.execute(sql)
    adresses = mycursor.fetchall()
    return render_template('participant/add_participant.html', adresses=adresses)


@app.route('/participant/add', methods=['POST'])
def valid_add_participant():
    prenom_participant = request.form.get('prenom_participant')
    nom_participant = request.form.get('nom_participant')
    adresse_mail_participant = request.form.get('adresse_mail_participant')
    telephone = request.form.get('telephone')
    present = 1 if request.form.get('present') else 0
    adresse_id = request.form.get('adresse_id')
    mycursor = get_db().cursor()
    tuple_param = (prenom_participant, nom_participant, adresse_mail_participant, telephone, present, adresse_id)
    sql = '''INSERT INTO participant(id_participant, prenom_participant, nom_participant, adresse_mail_participant, telephone, present, adresse_id)
    VALUES (NULL, %s, %s, %s, %s, %s, %s);'''
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/participant/show')


@app.route('/participant/edit', methods=['GET'])
def edit_participant():
    id = request.args.get('id')
    mycursor = get_db().cursor()
    sql = '''SELECT id_participant, prenom_participant, nom_participant, adresse_mail_participant, telephone, present, adresse_id
    FROM participant
    WHERE id_participant=%s;'''
    mycursor.execute(sql, (id,))
    participant = mycursor.fetchone()
    sql = '''SELECT id_adresse, nom_rue, numero_rue FROM adresse ORDER BY nom_rue;'''
    mycursor.execute(sql)
    adresses = mycursor.fetchall()
    return render_template('participant/edit_participant.html', participant=participant, adresses=adresses)


@app.route('/participant/edit', methods=['POST'])
def valid_edit_participant():
    id = request.form.get('id')
    prenom_participant = request.form.get('prenom_participant')
    nom_participant = request.form.get('nom_participant')
    adresse_mail_participant = request.form.get('adresse_mail_participant')
    telephone = request.form.get('telephone')
    present = 1 if request.form.get('present') else 0
    adresse_id = request.form.get('adresse_id')
    mycursor = get_db().cursor()
    tuple_param = (prenom_participant, nom_participant, adresse_mail_participant, telephone, present, adresse_id, id)
    sql = '''UPDATE participant
    SET prenom_participant = %s, nom_participant = %s, adresse_mail_participant = %s, telephone = %s, present = %s, adresse_id = %s
    WHERE id_participant=%s;'''
    mycursor.execute(sql, tuple_param)
    get_db().commit()
    return redirect('/participant/show')


@app.route('/participant/delete')
def delete_participant():
    id = request.args.get('id', 0)
    mycursor = get_db().cursor()
    tuple_param = (id,)
    mycursor.execute("DELETE FROM participer WHERE participant_id=%s;", tuple_param)
    mycursor.execute("DELETE FROM participant WHERE id_participant=%s;", tuple_param)
    get_db().commit()
    return redirect('/participant/show')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
