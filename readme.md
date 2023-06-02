Faire fonctionner la base de donnée SmartApp :
1. Installer un serveur MySql
(Uwamp, Xampp ou Mamp, etc).
2. Lancer le serveur MySql
Lancer le serveur et s'assurer que les voyants soient verts.
3. Importer le projet
Se rendre sur le lien gitlab et cloner le projet avec le lien HTTPS ensuite, aller sur PyCharm et cliquer sur get from VCS, coller le lien HTTPS puis cloner.
4. Importer la Base de données
Dans le répertoire racine du projet, ouvrir le fichier "ImportationDumpSql.py" et faire un "run".
En cas d'erreurs lors de l'importation, ouvrir le fichier ".env" à la racine du projet, contrôler les indications de connexion pour la bd.
5. Lancer le serveur flask et accéder à l'interface utilisateur
Dans le terminal cliquer sur le lien généré lors de l'éxécution du fichier "run_mon_app.py".
6. Accéder à l'interface utilisateur
Lors de la connection veuillez saisir "Olivier" comme pseudo et "Maccaud" comme mot de passe.
7. Edition
Vous pouvez maintenant entrer, modifier et supprimer des données à volonté.
INFOS
En cas de problème lors du login veuillez saisir l'url : http://127.0.0.1:5005/homepage
CONSEILS
En cas d'erreurs vérifier la version de python dans l'interpreter.
Redémarrer le serveur MySql.
En cas d'erreurs: ouvrir le fichier ".env" à la racine du projet, contrôler les indications de connexion pour la bd.
