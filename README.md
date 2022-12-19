


## WimsActivityViewer

Cette app permet de visualiser facilement l'activité des participants à une classe virtuelle Wims 
(voir [ici](https://wims.univ-mrs.fr/wims/) ou [là](https://wimsedu.info/))

Hébergé ici : [http://wimsactivityviewer.byache.fr/](http://wimsactivityviewer.byache.fr/)

Hébergement de secours sur alwaydata : [http://wimsactivityviewer.alwaysdata.net/](http://wimsactivityviewer.alwaysdata.net/)


## Déploiement local

1. créer un environement virtuel python: `virtualenv -P python3 venv`
2. l'activer: `source venv/bin/activate`
3. cloner le dépot git: `git clone https://github.com/byache/wimsActivityViewer.git`
4. se placer dans le dossier du dépot: `cd wimsActivityViewer`
5. installer les dépendances:`pip install -r requirements.txt`
5. indiquer le nom de l'app flask: `export FLASK_APP=wav.py`
6. activer le mode débug de flask: `export FLASK_ENV=development`
7. lancer le serveur local: `python3 -m flask run`

Normalement on a un retour du type :
```
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 172-164-488

```
Ouvrir l'url http://127.0.0.1:5000/ pour tester.

## Déploiement chez alwaysdata.net :

1. créer un compte chez alwaysdata :-)
2. se connecter en ssh
3. créer un venv, y installer uwsgi et les packages de requirements.txt
4. configurer un site wsgi dans le manager de alwaysdata


## TODO
Voir fichier TODO et éventuellement les issues
