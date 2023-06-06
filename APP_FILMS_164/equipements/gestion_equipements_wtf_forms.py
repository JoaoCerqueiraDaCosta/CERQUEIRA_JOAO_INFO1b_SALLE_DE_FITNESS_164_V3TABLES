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


class FormWTFAjouterequipements(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_equipements_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_equipements = StringField ("Nom", validators= [DataRequired(message="Veuillez entrer le Nom")])
    type_equipements = StringField ("Type", validators= [DataRequired(message="Veuillez entrer le Type")])
    date_achat_equipements = DateField ("Date d'achat", validators= [DataRequired(message="Veuillez entrer la date d'achat")])
    date_reparation_equipements = DateField ("Date de réparation", validators= [DataRequired(message="Veuillez entrer la date de réparation")])
    disponible_equipements = StringField ("Disponible", validators= [DataRequired(message="Veuillez entrer la disponibilité")])

    submit = SubmitField("Enregistrer l equipement")


class FormWTFUpdateequipements(FlaskForm):
    """
        Dans le formulaire "genre_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_equipements_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_equipements_update_wtf = StringField("Insérer l equipements ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_equipements_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    date_equipements_wtf_essai = DateField("Essai date", validators=[InputRequired("Date obligatoire"),
                                                               DataRequired("Date non valide")])
    submit = SubmitField("Update l equipements")


class FormWTFDeleteequipements(FlaskForm):
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
