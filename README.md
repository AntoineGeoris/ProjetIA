![Logo projet](https://i.ibb.co/ftvWCkY/258521491-421855366159472-2338510668152101421-n.png)

## Description du Projet
Projet de création d'une intelligence artificielle, réalisé en groupe de 3 étudiants.
Application web utilisant les framework [Flask](https://flask.palletsprojects.com/en/2.0.x/), [OWL](https://github.com/odoo/owl) ainsi que [SQLAlchemy](https://www.sqlalchemy.org/) (ORM).

L'IA se base sur un apprentissage par renforcement (Q-Function) :

- [Wikipedia](https://fr.wikipedia.org/wiki/Q-learning)
- [Youtube](https://www.youtube.com/watch?v=a0bVIyIJ074&t=747s)

## Description du jeu 
- Il s'agit d'un jeu de territoire.
- Le plateau comporte 5 x 5 territoires.
- Chaque tour un joueur peut se déplacer dans les limites du plateau, il est également permis de revenir sur un territoire précédemment capturé.
- Il n'est pas permis de voler un territoire à l'adversaire.
- Si des territoires (un ou plusieurs) deviennent inaccessibles pour l'un des joueurs, ils sont automatiquement annexés par l'autre joueur.
- Autrement dit, si l'un des joueurs entoure complètement (ou en utilisant les bords du plateau) des territoires, ces derniers lui sont automatiquement attribués.
![Initial](https://i.ibb.co/Cn8XZ2k/1.png)
![Enclos](https://i.ibb.co/gM9qQXZ/2.png)
![Capture](https://i.ibb.co/Y3XL15K/3.png)
- Une fois tous les territoires capturés, la partie prend fin.
- Le joueur comptabilisant le plus de territoire est déclaré vainqueur.

## Statut projet
### Requis
- [x] Squelette base de l'application
- [x] IA naive
- [x] Capture des enclos
- [x] Fin de partie
- [x] IA complète
- [x] Entrainement IA (en cours jusqu'à la remise de l'examen, la db ne sera pas update ici car github ne permet pas des fichiers trop volumineux)
- [x] Gestion des exceptions
- [x] Clean code (aurait pu mieux faire)
- [x] Dossier d'analyse
### Dossier d'analyse
- [x] Structure projet
- [x] Schéma DB final
- [x] Explication IA
- [x] Explication entrainement IA
- [x] Analyse reflexive 
- [x] Fonctionnalité supplémentaire
### Dépassement
- [x] Inscription et connexion
- [x] Gestion infos utilisateurs
- [ ] Partie / Utilisateurs
- [x] Décorateurs
- [ ] Page accueil remplie
- [ ] Optimisation apprentissage 
- [x] Documentation
- [ ] Déployer application
- [x] Fonctionnalité supplémentaire
### Optimisation 
- [ ] Enclos
### Modification nécessaire
- [ ] Méthode play dans la classe GameBoard (models.py)

## Installation & lancement
### Installation
- Un fichier requirements est disponible pour les dépendances :
	- pip3 install -r requirements.txt
### Lancement
- Lancer run.py
	- Via un interpréteur de commande, une fois dans le bon répertoire (.../ProjetIA) : python run.py

	- Il est également possible de définir des variables via Flask : [Plus d'informations](https://flask.palletsprojects.com/en/2.0.x/cli/)

- Le site est accesible via http://localhost:5000/



