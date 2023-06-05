"""Gestion des "routes" FLASK et des données pour les membres_avoir_coach.
Fichier : gestion_membres_avoir_coach_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.membres_avoir_coach.gestion_membres_avoir_coach_wtf_forms import FormWTFAjouterGenres
from APP_FILMS_164.membres_avoir_coach.gestion_membres_avoir_coach_wtf_forms import FormWTFDeleteGenre
from APP_FILMS_164.membres_avoir_coach.gestion_membres_avoir_coach_wtf_forms import FormWTFUpdateGenre

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /membres_avoir_coach_afficher
    
    Test : ex : http://127.0.0.1:5575/membres_avoir_coach_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_membres_avoir_coach_sel = 0 >> tous les membres_avoir_coach.
                id_membres_avoir_coach_sel = "n" affiche le membres_avoir_coach dont l'id est "n"
"""


@app.route("/membres_avoir_coach_afficher/<string:order_by>/<int:id_membres_avoir_coach_sel>", methods=['GET', 'POST'])
def membres_avoir_coach_afficher(order_by, id_membres_avoir_coach_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_membres_avoir_coach_sel == 0:
                    strsql_membres_avoir_coach_afficher = """SELECT ID_membres_avoir_coach, t_membres.prenom AS prenom_membres, t_membres.nom AS nom_membres, t_coach.prenom AS prenom_coach, t_coach.nom AS nom_coach FROM t_membres_avoir_coach
INNER JOIN t_coach ON t_coach.ID_coach = t_membres_avoir_coach.fk_coach
INNER JOIN t_membres ON t_membres.id_membres = t_membres_avoir_coach.fk_membres"""
                    mc_afficher.execute(strsql_membres_avoir_coach_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_membres_avoir_coach"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du membres_avoir_coach sélectionné avec un nom de variable
                    valeur_id_membres_avoir_coach_selected_dictionnaire = {"value_id_membres_avoir_coach_selected": id_membres_avoir_coach_sel}
                    strsql_membres_avoir_coach_afficher = """SELECT ID_membres_avoir_coach, t_membres.prenom AS prenom_membres, t_membres.nom AS nom_membres, t_coach.prenom AS prenom_coach, t_coach.nom AS nom_coach FROM t_membres_avoir_coach
INNER JOIN t_coach ON t_coach.ID_coach = t_membres_avoir_coach.fk_coach
INNER JOIN t_membres ON t_membres.id_membres = t_membres_avoir_coach.fk_membres where id_membres_avoir_coach =%(value_id_membres_avoir_coach_selected)s"""

                    mc_afficher.execute(strsql_membres_avoir_coach_afficher, valeur_id_membres_avoir_coach_selected_dictionnaire)
                else:
                    strsql_membres_avoir_coach_afficher = """SELECT ID_membres_avoir_coach, t_membres.prenom AS prenom_membres, t_membres.nom AS nom_membres, t_coach.prenom AS prenom_coach, t_coach.nom AS nom_coach FROM t_membres_avoir_coach
INNER JOIN t_coach ON t_coach.ID_coach = t_membres_avoir_coach.fk_coach
INNER JOIN t_membres ON t_membres.id_membres = t_membres_avoir_coach.fk_membres"""

                    mc_afficher.execute(strsql_membres_avoir_coach_afficher)

                data_membres_avoir_coach = mc_afficher.fetchall()

                print("data_membres_avoir_coach ", data_membres_avoir_coach, " Type : ", type(data_membres_avoir_coach))

        except Exception as Exception_membres_avoir_coach_afficher:
            raise Exception_membres_avoir_coach_afficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{membres_avoir_coach_afficher.__name__} ; "
                                          f"{Exception_membres_avoir_coach_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("/membres_avoir_coach/membres_avoir_coach_afficher.html", data=data_membres_avoir_coach)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /membres_avoir_coach_ajouter
    
    Test : ex : http://127.0.0.1:5575/membres_avoir_coach_ajouter
    
    Paramètres : sans
    
    But : Ajouter un membres_avoir_coach pour un film
    
    Remarque :  Dans le champ "name_membres_avoir_coach_html" du formulaire "membres_avoir_coach/membres_avoir_coach_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/membres_avoir_coach_ajouter", methods=['GET', 'POST'])
def membres_avoir_coach_ajouter_wtf():
    form = FormWTFAjoutermembres_avoir_coach()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                name_membres_avoir_coach_wtf = form.nom_membres_avoir_coach_wtf.data
                name_membres_avoir_coach = name_membres_avoir_coach_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_intitule_membres_avoir_coach": name_membres_avoir_coach}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_membres_avoir_coach = """INSERT INTO t_membres_avoir_coach (id_membres_avoir_coach,intitule_membres_avoir_coach) VALUES (NULL,%(value_intitule_membres_avoir_coach)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_membres_avoir_coach, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('membres_avoir_coach_afficher', order_by='DESC', id_membres_avoir_coach_sel=0))

        except Exception as Exception_membres_avoir_coach_ajouter_wtf:
            raise Exceptionmembres_avoir_coachAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{membres_avoir_coach_ajouter_wtf.__name__} ; "
                                            f"{Exception_membres_avoir_coach_ajouter_wtf}")

    return render_template("membres_avoir_coach/membres_avoir_coach_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /membres_avoir_coach_update
    
    Test : ex cliquer sur le menu "membres_avoir_coach" puis cliquer sur le bouton "EDIT" d'un "membres_avoir_coach"
    
    Paramètres : sans
    
    But : Editer(update) un membres_avoir_coach qui a été sélectionné dans le formulaire "membres_avoir_coach_afficher.html"
    
    Remarque :  Dans le champ "nom_membres_avoir_coach_update_wtf" du formulaire "membres_avoir_coach/membres_avoir_coach_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/membres_avoir_coach_update", methods=['GET', 'POST'])
def membres_avoir_coach_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_membres_avoir_coach"
    id_membres_avoir_coach_update = request.values['id_membres_avoir_coach_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdatemembres_avoir_coach()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update.submit.data:
            # Récupèrer la valeur du champ depuis "membres_avoir_coach_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_membres_avoir_coach_update = form_update.nom_membres_avoir_coach_update_wtf.data
            name_membres_avoir_coach_update = name_membres_avoir_coach_update.lower()
            date_membres_avoir_coach_essai = form_update.date_membres_avoir_coach_wtf_essai.data

            valeur_update_dictionnaire = {"value_id_membres_avoir_coach": id_membres_avoir_coach_update,
                                          "value_name_membres_avoir_coach": name_membres_avoir_coach_update,
                                          "value_date_membres_avoir_coach_essai": date_membres_avoir_coach_essai
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulemembres_avoir_coach = """UPDATE t_membres_avoir_coach SET intitule_membres_avoir_coach = %(value_name_membres_avoir_coach)s, 
            date_ins_membres_avoir_coach = %(value_date_membres_avoir_coach_essai)s WHERE id_membres_avoir_coach = %(value_id_membres_avoir_coach)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulemembres_avoir_coach, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_membres_avoir_coach_update"
            return redirect(url_for('membres_avoir_coach_afficher', order_by="ASC", id_membres_avoir_coach_sel=id_membres_avoir_coach_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_membres_avoir_coach" et "intitule_membres_avoir_coach" de la "t_membres_avoir_coach"
            str_sql_id_membres_avoir_coach = "SELECT * FROM t_coach " \
                               "WHERE id_membres_avoir_coach = %(value_id_membres_avoir_coach)s"
            valeur_select_dictionnaire = {"value_id_membres_avoir_coach": id_membres_avoir_coach_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_membres_avoir_coach, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom membres_avoir_coach" pour l'UPDATE
            data_nom_membres_avoir_coach = mybd_conn.fetchone()
            print("data_nom_membres_avoir_coach ", data_nom_membres_avoir_coach, " type ", type(data_nom_membres_avoir_coach), " membres_avoir_coach ",
                  data_nom_membres_avoir_coach["intitule_membres_avoir_coach"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "membres_avoir_coach_update_wtf.html"
            form_update.nom_membres_avoir_coach_update_wtf.data = data_nom_membres_avoir_coach["intitule_membres_avoir_coach"]
            form_update.date_membres_avoir_coach_wtf_essai.data = data_nom_membres_avoir_coach["date_ins_membres_avoir_coach"]

    except Exception as Exception_membres_avoir_coach_update_wtf:
        raise Exceptionmembres_avoir_coachUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{membres_avoir_coach_update_wtf.__name__} ; "
                                      f"{Exception_membres_avoir_coach_update_wtf}")

    return render_template("membres_avoir_coach/membres_avoir_coach_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /membres_avoir_coach_delete
    
    Test : ex. cliquer sur le menu "membres_avoir_coach" puis cliquer sur le bouton "DELETE" d'un "membres_avoir_coach"
    
    Paramètres : sans
    
    But : Effacer(delete) un membres_avoir_coach qui a été sélectionné dans le formulaire "membres_avoir_coach_afficher.html"
    
    Remarque :  Dans le champ "nom_membres_avoir_coach_delete_wtf" du formulaire "membres_avoir_coach/membres_avoir_coach_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/membres_avoir_coach_delete", methods=['GET', 'POST'])
def membres_avoir_coach_delete_wtf():
    data_films_attribue_membres_avoir_coach_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_membres_avoir_coach"
    id_membres_avoir_coach_delete = request.values['id_membres_avoir_coach_btn_delete_html']

    # Objet formulaire pour effacer le membres_avoir_coach sélectionné.
    form_delete = FormWTFDeletemembres_avoir_coach()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("membres_avoir_coach_afficher", order_by="ASC", id_membres_avoir_coach_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "membres_avoir_coach/membres_avoir_coach_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_membres_avoir_coach_delete = session['data_films_attribue_membres_avoir_coach_delete']
                print("data_films_attribue_membres_avoir_coach_delete ", data_films_attribue_membres_avoir_coach_delete)

                flash(f"Effacer le membres_avoir_coach de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer membres_avoir_coach" qui va irrémédiablement EFFACER le membres_avoir_coach
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_membres_avoir_coach": id_membres_avoir_coach_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_membres_avoir_coach = """DELETE FROM t_membres_avoir_coach_film WHERE fk_membres_avoir_coach = %(value_id_membres_avoir_coach)s"""
                str_sql_delete_idmembres_avoir_coach = """DELETE FROM t_membres_avoir_coach WHERE id_membres_avoir_coach = %(value_id_membres_avoir_coach)s"""
                # Manière brutale d'effacer d'abord la "fk_membres_avoir_coach", même si elle n'existe pas dans la "t_membres_avoir_coach_film"
                # Ensuite on peut effacer le membres_avoir_coach vu qu'il n'est plus "lié" (INNODB) dans la "t_membres_avoir_coach_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_membres_avoir_coach, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idmembres_avoir_coach, valeur_delete_dictionnaire)

                flash(f"membres_avoir_coach définitivement effacé !!", "success")
                print(f"membres_avoir_coach définitivement effacé !!")

                # afficher les données
                return redirect(url_for('membres_avoir_coach_afficher', order_by="ASC", id_membres_avoir_coach_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_membres_avoir_coach": id_membres_avoir_coach_delete}
            print(id_membres_avoir_coach_delete, type(id_membres_avoir_coach_delete))

            # Requête qui affiche tous les films_membres_avoir_coach qui ont le membres_avoir_coach que l'utilisateur veut effacer
            str_sql_membres_avoir_coach_films_delete = """SELECT id_membres_avoir_coach_film, nom_film, id_membres_avoir_coach, intitule_membres_avoir_coach FROM t_membres_avoir_coach_film 
                                            INNER JOIN t_film ON t_membres_avoir_coach_film.fk_film = t_film.id_film
                                            INNER JOIN t_membres_avoir_coach ON t_membres_avoir_coach_film.fk_membres_avoir_coach = t_membres_avoir_coach.id_membres_avoir_coach
                                            WHERE fk_membres_avoir_coach = %(value_id_membres_avoir_coach)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_membres_avoir_coach_films_delete, valeur_select_dictionnaire)
                data_films_attribue_membres_avoir_coach_delete = mydb_conn.fetchall()
                print("data_films_attribue_membres_avoir_coach_delete...", data_films_attribue_membres_avoir_coach_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "membres_avoir_coach/membres_avoir_coach_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_membres_avoir_coach_delete'] = data_films_attribue_membres_avoir_coach_delete

                # Opération sur la BD pour récupérer "id_membres_avoir_coach" et "intitule_membres_avoir_coach" de la "t_membres_avoir_coach"
                str_sql_id_membres_avoir_coach = "SELECT SELECT * FROM t_coach"

                mydb_conn.execute(str_sql_id_membres_avoir_coach, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom membres_avoir_coach" pour l'action DELETE
                data_nom_membres_avoir_coach = mydb_conn.fetchone()
                print("data_nom_membres_avoir_coach ", data_nom_membres_avoir_coach, " type ", type(data_nom_membres_avoir_coach), " membres_avoir_coach ",
                      data_nom_membres_avoir_coach["intitule_membres_avoir_coach"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "membres_avoir_coach_delete_wtf.html"
            form_delete.nom_membres_avoir_coach_delete_wtf.data = data_nom_membres_avoir_coach["intitule_membres_avoir_coach"]

            # Le bouton pour l'action "DELETE" dans le form. "membres_avoir_coach_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_membres_avoir_coach_delete_wtf:
        raise Exceptionmembres_avoir_coachDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{membres_avoir_coach_delete_wtf.__name__} ; "
                                      f"{Exception_membres_avoir_coach_delete_wtf}")

    return render_template("membres_avoir_coach/membres_avoir_coach_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_membres_avoir_coach_delete)
