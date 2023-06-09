"""
    Fichier : gestion_genres_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormWTFAjoutermembres(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_equipements_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    prenom_membres = StringField ("Prénom", validators= [DataRequired(message="Veuillez entrer le Prénom")])
    nom_membres = StringField ("Nom", validators= [DataRequired(message="Veuillez entrer le Nom")])
    date_naissance_membres = DateField ("Date de Naissance", validators= [DataRequired(message="Veuillez entrer une date")])
    email_membres = StringField ("Email", validators= [DataRequired(message="Veuillez entrer l'email")])
    telephone_membres = StringField ("Téléphone", validators= [DataRequired(message="Veuillez entrer le numéro de téléphone")])
    date_inscription_membres = DateField ("Date d'inscription", validators= [DataRequired(message="Veuiller entrez la date d'inscription")])
    actif_membres = StringField ("Actif", validators= [DataRequired(message="Veuillez entrer si le membres est actif")])

    submit = SubmitField("Enregistrer le nouveau membre")


class FormWTFUpdateMembres(FlaskForm):
    """
        Dans le formulaire "genre_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_equipements_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    prenom_membres_update = StringField("Prénom", validators=[DataRequired(message="Veuillez entrer le Prénom")])
    nom_membres_update  = StringField("Nom", validators=[DataRequired(message="Veuillez entrer le Nom")])
    date_naissance_membres_update  = DateField("Date de Naissance", validators=[DataRequired(message="Veuillez entrer une date")])
    email_membres_update  = StringField("Email", validators=[DataRequired(message="Veuillez entrer l'email")])
    telephone_membres_update  = StringField("Téléphone",
                                    validators=[DataRequired(message="Veuillez entrer le numéro de téléphone")])
    date_inscription_membres_update  = DateField("Date d'inscription",
                                         validators=[DataRequired(message="Veuiller entrez la date d'inscription")])
    actif_membres_update  = StringField("Actif", validators=[DataRequired(message="Veuillez entrer si le membres est actif")])

    submit = SubmitField("Update l equipements")


class FormWTFDeletemembres(FlaskForm):
    """
        Dans le formulaire "genre_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_equipements_delete_wtf = StringField("Effacer cet equipement")
    submit_btn_del = SubmitField("Effacer cet equipements")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
