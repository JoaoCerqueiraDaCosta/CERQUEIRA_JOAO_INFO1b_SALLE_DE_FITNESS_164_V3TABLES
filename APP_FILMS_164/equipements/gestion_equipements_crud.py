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
from APP_FILMS_164.equipements.gestion_equipements_wtf_forms import FormWTFAjouterequipements
from APP_FILMS_164.equipements.gestion_equipements_wtf_forms import FormWTFDeleteequipements
from APP_FILMS_164.equipements.gestion_equipements_wtf_forms import FormWTFUpdateequipements

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /equipements_afficher
    
    Test : ex : http://127.0.0.1:5575/equipements_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_equipements_sel = 0 >> tous les equipements.
                id_equipements_sel = "n" affiche le equipements dont l'id est "n"
"""


@app.route("/equipements_afficher/<string:order_by>/<int:id_equipements_sel>", methods=['GET', 'POST'])
def equipements_afficher(order_by, id_equipements_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_equipements_sel == 0:
                    strsql_equipements_afficher = """SELECT * FROM t_equipements"""
                    mc_afficher.execute(strsql_equipements_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_equipements_selected_dictionnaire = {"value_id_equipements_selected": id_equipements_sel}
                    strsql_equipements_afficher = """SELECT * FROM t_equipements where id_equipements =%(value_id_equipements_selected)s"""

                    mc_afficher.execute(strsql_equipements_afficher, valeur_id_equipements_selected_dictionnaire)
                else:
                    strsql_equipements_afficher = """SELECT * FROM t_equipements"""

                    mc_afficher.execute(strsql_equipements_afficher)

                data_equipements = mc_afficher.fetchall()

                print("data_equipements ", data_equipements, " Type : ", type(data_equipements))

        except Exception as Exception_equipements_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{equipements_afficher.__name__} ; "
                                          f"{Exception_equipements_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("/equipements/equipements_afficher.html", data=data_equipements)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /Equipements_ajouter
    
    Test : ex : http://127.0.0.1:5575/genres_ajouter
    
    Paramètres : sans
    
    But : Ajouter un Equipement
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "genres/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/equipements_ajouter", methods=['GET', 'POST'])
def equipements_ajouter_wtf():
    form = FormWTFAjouterequipements()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                name_equipements_wtf = form.nom_equipements_wtf.data
                name_equipements = name_equipements_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_intitule_equipements": name_equipements}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_equipements = """INSERT INTO t_equipements (id_equipements,intitule_equipements) VALUES (NULL,%(value_intitule_equipements)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_equipements, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('equipements_afficher', order_by='DESC', id_equipements_sel=0))

        except Exception as Exception_equipements_ajouter_wtf:
            raise Exception_equipements_ajouter_wtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{equipements_ajouter_wtf.__name__} ; "
                                            f"{Exception_equipements_ajouter_wtf}")

    return render_template("/equipements_ajouter_wtf.html", form=form)


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


@app.route("/equipements_update", methods=['GET', 'POST'])
def equipements_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_equipements_update = request.values['id_equipements_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateequipements()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update.submit.data:
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_equipements_update = form_update.nom_equipements_update_wtf.data
            name_equipements_update = name_equipements_update.lower()
            date_equipements_essai = form_update.date_equipements_wtf_essai.data

            valeur_update_dictionnaire = {"value_id_equipements": id_equipements_update,
                                          "value_name_equipements": name_equipements_update,
                                          "value_date_equipements_essai": date_equipements_essai
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intituleequipements = """UPDATE t_equipements SET intitule_equipements = %(value_name_equipements)s, 
            date_ins_equipements = %(value_date_equipements_essai)s WHERE id_equipements = %(value_id_equipements)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intituleequipements, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('equipements_afficher', order_by="ASC", id_equipements_sel=id_equipements_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_equipements = "SELECT * FROM t_equipements " \
                               "WHERE id_equipements = %(value_id_equipements)s"
            valeur_select_dictionnaire = {"value_id_equipements": id_equipements_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_equipements, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_equipements = mybd_conn.fetchone()
            print("data_nom_equipements ", data_nom_equipements, " type ", type(data_nom_equipements), " equipements ",
                  data_nom_equipements["intitule_equipements"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "genre_update_wtf.html"
            form_update.nom_equipements_update_wtf.data = data_nom_equipements["intitule_equipements"]
            form_update.date_equipements_wtf_essai.data = data_nom_equipements["date_ins_equipements"]

    except Exception as Exception_equipements_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{equipements_update_wtf.__name__} ; "
                                      f"{Exception_equipements_update_wtf}")

    return render_template("equipements_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "genres/genre_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/equipements_delete", methods=['GET', 'POST'])
def equipements_delete_wtf():
    data_films_attribue_equipements_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_equipements"
    id_equipements_delete = request.values['id_equipements_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteequipements()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("equipements_afficher", order_by="ASC", id_equipements_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_equipements_delete = session['data_films_attribue_equipements_delete']
                print("data_films_attribue_equipements_delete ", data_films_attribue_equipements_delete)

                flash(f"Effacer le equipements de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_equipements": id_equipements_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_equipements = """DELETE FROM t_equipements WHERE fk_equipements = %(value_id_equipements)s"""
                str_sql_delete_idequipements = """DELETE FROM t_equipements WHERE id_equipements = %(value_id_equipements)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_equipements, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idequipements, valeur_delete_dictionnaire)

                flash(f"equipements définitivement effacé !!", "success")
                print(f"equipements définitivement effacé !!")

                # afficher les données
                return redirect(url_for('equipements_afficher', order_by="ASC", id_equipements_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_equipements": id_equipements_delete}
            print(id_equipements_delete, type(id_equipements_delete))

            # Requête qui affiche tous les films_genres qui ont le genre que l'utilisateur veut effacer
            str_sql_equipements_delete = """SELECT id_equipements, nom_film, id_equipements, intitule_equipements FROM t_equipements_film 
                                            INNER JOIN t_film ON t_equipements.fk_film = t_film.id_film
                                            INNER JOIN t_equipements ON t_equipements_film.fk_equipements = t_equipements.id_equipements
                                            WHERE fk_equipements = %(value_id_equipements)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_equipements_delete, valeur_select_dictionnaire)
                data_films_attribue_genre_delete = mydb_conn.fetchall()
                print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
                str_sql_id_equipements = "SELECT SELECT * FROM t_equipements"

                mydb_conn.execute(str_sql_id_equipements, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_nom_equipements = mydb_conn.fetchone()
                print("data_nom_equipements ", data_nom_equipements, " type ", type(data_nom_equipements), " equipements ",
                      data_nom_equipements["intitule_equipements"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "genre_delete_wtf.html"
            form_delete.nom_equipements_delete_wtf.data = data_nom_equipements["intitule_equipements"]

            # Le bouton pour l'action "DELETE" dans le form. "genre_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_equipements_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{equipements_delete_wtf.__name__} ; "
                                      f"{Exception_equipements_delete_wtf}")

    return render_template("equipements_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_equipements_delete)
