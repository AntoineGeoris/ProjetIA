# ProjetIA - Maki
![Logo projet](https://i.ibb.co/ftvWCkY/258521491-421855366159472-2338510668152101421-n.png) Format: ![Alt Text](url)

## Description du Projet
Projet de création d'une intelligence artificielle, réalisé en groupe de 3 étudiants.
Application web utilisant les framework Flask, OWL ainsi que SQLAlchemy (ORM).


## Description du jeu 
- Il s'agit d'un jeu de territoire.
- Le plateau comporte 5 x 5 territoires.
- Chaque tour un joueur peut se déplacer dans les limites du plateau, il est également permis de revenir sur un territoire précédemment capturé.
- Il n'est pas permis de voler un territoire à l'adversaire.
- Si des territoires (un ou plusieurs) deviennent inaccessibles pour l'un des joueurs, ils sont automatiquement annexés par l'autre joueur.
  Autrement dit, si l'un des joueurs entoure complètement (ou en utilisant les bords du plateau) une partie de territoire, ces derniers lui sont automatiquement attribués.
![Etat initial](https://i.ibb.co/Cn8XZ2k/1.png) Format: ![Alt Text](url) 
![Mouvement](https://i.ibb.co/gM9qQXZ/2.png) Format: ![Alt Text](url) 
![Capture](https://i.ibb.co/Y3XL15K/3.png) Format: ![Alt Text](url) 
- Une fois tous les territoires capturés, la partie prend fin.
- Le joueur comptabilisant le plus de territoire est déclaré vainqueur.

## Statut projet
### Requis
- [x] Squelette base de l'application
- [x] IA naive
- [x] Capture des enclos
- [ ] Fin de partie
- [ ] IA complète
- [ ] Entrainement IA
- [ ] Gestion des exceptions
### Dépassement
- [ ] Inscription et connexion
- [ ] Optimisation apprentissage 
- [ ] Documentation
- [ ] Déployer application

## Installation & lancement

Un fichier requirements est disponible pour les dépendances :
pip3 install -r requirements.txt

Lancer run.py

Accesible via http://localhost:5000/


