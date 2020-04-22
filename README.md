


## WimsActivityViewer

Cette app permet de visualiser facilement l'activité des participants à une classe virtuelle Wims 
(voir [ici](https://wims.univ-mrs.fr/wims/) ou [là](https://wimsedu.info/))

Hébergé sur ...

## Utilisation en local

1. Téléchargez les fichier de ce dépôt
2. Téléchargez une sauvegarde zip de votre classe wims dans le même dossier.
3. Exécutez le fichier wav.py
4. Les fichiers .rtf et .html qui ont été générés automatiquement contiennent des visualisations de l'activité des participants.
Il n'y a plus qu'à leur imprimer et leur distibuer, après avoir écrit pour chacun une observation concernant leur travail et/ou leur
méthode.


## Déploiement local

1. créer un environement virtuel python: `virtualenv -P python3 venv`
2. l'activer: `source venv/bin/activate`
3. cloner le dépot git: `git clone https://github.com/......git`
4. se placer dans le dossier du dépot: `cd .....`
5. installer les dépendances:`pip install -r requirements.txt`
5. indiquer le nom de l'app flask: `export FLASK_APP=wav.py`
6. activer le mode débug de flask: `export FLASK_ENV=development`
7. lancer le serveur local: `python -m flask run`

Normalement on a un retour du type:
```
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 172-164-488

```
Ouvrir l'url http://127.0.0.1:5000/ pour tester.

## TODO
Voir fichier TODO et éventuellement les issues
