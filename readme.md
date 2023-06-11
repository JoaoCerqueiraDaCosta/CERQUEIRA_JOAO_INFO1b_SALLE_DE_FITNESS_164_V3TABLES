Pour faire fonctionner la base de données, suivez ces étapes :

Installation du serveur MySQL (Laragon).

Lancement du serveur MySQL et de Laragon.

Importation du projet :
a. Rendez-vous sur le lien GitHub et clonez le projet en utilisant le lien HTTPS.
b. Ouvrez PyCharm, cliquez sur "Get from VCS", collez le lien HTTPS et clonez le projet.

Importation de la base de données :
a. Dans le répertoire racine du projet, ouvrez le fichier "ImportationDumpSql.py" et exécutez-le.
b. Si des erreurs surviennent lors de l'importation, ouvrez le fichier ".env" à la racine du projet et vérifiez les informations de connexion à la base de données.

Exécution de la requête pour afficher les données de la base de données MySQL.
Utilisez le fichier "2_test_connection_bd.py".

Lancement du serveur Flask et accès à l'interface utilisateur :
Dans le terminal, cliquez sur le lien généré lors de l'exécution du fichier "run_mon_app.py".

Accès à l'interface utilisateur.

Édition :
Vous pouvez maintenant entrer, modifier et supprimer des données selon vos besoins.

INFORMATIONS :
Si vous rencontrez des problèmes lors de la connexion, veuillez utiliser l'URL suivante : http://127.0.0.1:5005/homepage.

CONSEILS :

Vérifiez la version de Python dans l'interpréteur en cas d'erreurs.
Redémarrez le serveur MySQL si nécessaire.
En cas d'erreurs persistantes, vérifiez les informations de connexion à la base de données dans le fichier ".env" à la racine du projet.
