"""Gestion des "routes" FLASK et des données pour les genres.
Fichier : gestion_genres_crud.py
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
from APP_FILMS_164.membres.gestion_membres_wtf_forms import FormWTFAjoutermembres
from APP_FILMS_164.membres.gestion_membres_wtf_forms import FormWTFDeletemembres
from APP_FILMS_164.membres.gestion_membres_wtf_forms import FormWTFUpdatemembres

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /membres_afficher
    
    Test : ex : http://127.0.0.1:5575/membres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_membres_sel = 0 >> tous les membres.
                id_membres_sel = "n" affiche le membres dont l'id est "n"
"""


@app.route("/membres_afficher/<string:order_by>/<int:id_membres_sel>", methods=['GET', 'POST'])
def membres_afficher(order_by, id_membres_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_membres_sel == 0:
                    strsql_membres_afficher = """SELECT * FROM t_membres"""
                    mc_afficher.execute(strsql_membres_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_membres_selected_dictionnaire = {"value_id_membres_selected": id_membres_sel}
                    strsql_membres_afficher = """SELECT * FROM t_membres where id_membres =%(value_id_membres_selected)s"""

                    mc_afficher.execute(strsql_membres_afficher, valeur_id_membres_selected_dictionnaire)
                else:
                    strsql_membres_afficher = """SELECT * FROM t_membres"""

                    mc_afficher.execute(strsql_membres_afficher)

                data_membres = mc_afficher.fetchall()

                print("data_membres ", data_membres, " Type : ", type(data_membres))

        except Exception as Exception_membres_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{membres_afficher.__name__} ; "
                                          f"{Exception_membres_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("/membres/membres_afficher.html", data=data_membres)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter
    
    Test : ex : http://127.0.0.1:5575/genres_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un film
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "genres/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/membres_ajouter", methods=['GET', 'POST'])
def membres_ajouter_wtf():
    form = FormWTFAjoutermembres()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                name_membres_wtf = form.nom_membres_wtf.data
                name_membres = name_membres_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_intitule_membres": name_membres}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_membres = """INSERT INTO t_membres (id_membres,intitule_membres) VALUES (NULL,%(value_intitule_membres)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_membres, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('membres_afficher', order_by='DESC', id_membres_sel=0))

        except Exception as Exception_membres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{membres_ajouter_wtf.__name__} ; "
                                            f"{Exception_membres_ajouter_wtf}")

    return render_template("membres_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update
    
    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "genres/genre_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/membres_update", methods=['GET', 'POST'])
def membres_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_membres_update = request.values['id_membres_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateGenre()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update.submit.data:
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_membres_update = form_update.nom_membres_update_wtf.data
            name_membres_update = name_membres_update.lower()
            date_membres_essai = form_update.date_membres_wtf_essai.data

            valeur_update_dictionnaire = {"value_id_membres": id_membres_update,
                                          "value_name_membres": name_membres_update,
                                          "value_date_membres_essai": date_membres_essai
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulemembres = """UPDATE t_membres SET intitule_membres = %(value_name_membres)s, 
            date_ins_membres = %(value_date_membres_essai)s WHERE id_membres = %(value_id_membres)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulemembres, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('membres_afficher', order_by="ASC", id_membres_sel=id_membres_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_membres = "SELECT * FROM t_membres " \
                               "WHERE id_membres = %(value_id_membres)s"
            valeur_select_dictionnaire = {"value_id_membres": id_membres_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_membres, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_membres = mybd_conn.fetchone()
            print("data_nom_membres ", data_nom_membres, " type ", type(data_nom_membres), " membres ",
                  data_nom_membres["intitule_membres"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "genre_update_wtf.html"
            form_update.nom_membres_update_wtf.data = data_nom_membres["intitule_membres"]
            form_update.date_membres_wtf_essai.data = data_nom_membres["date_ins_membres"]

    except Exception as Exception_membres_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{membres_update_wtf.__name__} ; "
                                      f"{Exception_membres_update_wtf}")

    return render_template("membres_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "genres/genre_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/membres_delete", methods=['GET', 'POST'])
def membres_delete_wtf():
    data_films_attribue_membres_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_membres"
    id_membres_delete = request.values['id_membres_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeletemembres()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("membres_afficher", order_by="ASC", id_membres_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_membres_delete = session['data_films_attribue_membres_delete']
                print("data_films_attribue_membres_delete ", data_films_attribue_membres_delete)

                flash(f"Effacer le membres de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_membres": id_membres_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_membres = """DELETE FROM t_membres WHERE fk_membres = %(value_id_membres)s"""
                str_sql_delete_idmembres = """DELETE FROM t_membres WHERE id_membres = %(value_id_membres)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_membres, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idmembres, valeur_delete_dictionnaire)

                flash(f"membres définitivement effacé !!", "success")
                print(f"membres définitivement effacé !!")

                # afficher les données
                return redirect(url_for('membres_afficher', order_by="ASC", id_membres_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_membres": id_membres_delete}
            print(id_membres_delete, type(id_membres_delete))

            # Requête qui affiche tous les films_genres qui ont le genre que l'utilisateur veut effacer
            str_sql_membres_films_delete = """SELECT id_membres, nom_film, id_membres, intitule_membres FROM t_membres_film 
                                            INNER JOIN t_film ON t_membres.fk_film = t_film.id_film
                                            INNER JOIN t_membres ON t_membres_film.fk_membres = t_membres.id_membres
                                            WHERE fk_membres = %(value_id_membres)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_membres_delete, valeur_select_dictionnaire)
                data_films_attribue_genre_delete = mydb_conn.fetchall()
                print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
                str_sql_id_membres = "SELECT SELECT * FROM t_membres"

                mydb_conn.execute(str_sql_id_membres, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_nom_membres = mydb_conn.fetchone()
                print("data_nom_membres ", data_nom_membres, " type ", type(data_nom_membres), " membres ",
                      data_nom_membres["intitule_membres"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "genre_delete_wtf.html"
            form_delete.nom_membres_delete_wtf.data = data_nom_membres["intitule_membres"]

            # Le bouton pour l'action "DELETE" dans le form. "genre_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_membres_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{membres_delete_wtf.__name__} ; "
                                      f"{Exception_membres_delete_wtf}")

    return render_template("membres_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_membres_delete)