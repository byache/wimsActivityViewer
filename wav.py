#! /usr/bin/env python3
# coding: utf8
# ce fichier est le fichier principal (l'app)

import os
from time import time
from shutil import rmtree
from flask import Flask, flash, request, redirect, url_for, render_template, session, send_from_directory
from werkzeug.utils import secure_filename
from io import BytesIO
from datafactory import * #contient des fonctions enlevées d'ici pour ne pas surcharger...
from uuid import uuid4

UPLOAD_FOLDER = 'tmp'
ALLOWED_EXTENSIONS = {'zip'}

app = Flask(__name__)
app.secret_key = 'GZD9qr}3Q]9p7iW._5?s'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 #max size 10 Mo

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    
def cleanData(session):
    #supprime le dossier de la session 'session'
    rmtree(os.path.join(app.config['UPLOAD_FOLDER'], session))
    #os.rmdir(os.path.join(app.config['UPLOAD_FOLDER'], session))

def cleanAllData(duration=3600):
    #supprime tous les fichiers de 'tmp' non modifiés depuis 'duration' secondes
    t_limite = time() - duration
    sessions = os.listdir(app.config['UPLOAD_FOLDER'])
    for s in sessions:
        if os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], s)) < t_limite :
            cleanData(s)

@app.route('/tmp/<session>/<titre>')
def download_file(session,titre):
    uploads = os.path.join(app.config['UPLOAD_FOLDER'], session)
    return send_from_directory(directory=uploads, filename=titre)

@app.route('/', methods=['GET', 'POST'])
def main_function():
    # on crée le répertoire tmp s'il n'existe pas déjà
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    # on nettoie les sessions trop vieilles (+ de 1h)
    cleanAllData(3600)
    
    # on regarde si c'est la première page qui est vue dans la session
    if 'pseudo' not in session :
        # si oui, on attribue un numéro aléatoire unique de session et on le stocke dans le cookie 'pseudo'
        pseudo = uuid4().hex
        session['pseudo'] = pseudo
        #session['page'] = "accueil"
        #on crée un répertoire avec le numéro de session dans 'tmp'
        dirname = secure_filename(pseudo)
        dirpath = os.path.join(app.config['UPLOAD_FOLDER'], dirname)
        os.mkdir(dirpath,0o755)

        
    pseudo = session['pseudo']
    dirname = secure_filename(pseudo)
    dirpath = os.path.join(app.config['UPLOAD_FOLDER'], dirname)
    #crée le répertoire s'il n'existe pas déjà (inutile à priori, mais bon... )
    os.makedirs(dirpath, exist_ok=True)
    zipname = os.path.join(dirpath,'class.zip')
    #succession des vues : ["accueil","feuille","result"]
    try:
        page = request.form['page']
    except:
        page = 'accueil'
    feuilles = []
    
    if request.method == 'POST' and page == 'feuille':
        # check if the post request has the file part          -------> ne marche pas !!
        if 'file' not in request.files and not os.path.isfile(zipname):
            flash('Aucun fichier sélectionné')
            #session['page'] = "accueil"
            return redirect(request.url)
        if 'file' not in request.files and os.path.isfile(zipname):
            try:
                feuilles = fsheets(zipname)
            except:
                flash("Votre zip ne semble pas être une sauvegarde de classe Wims. Erreur de fichier ?")
                return redirect(request.url)
        if 'file' in request.files:
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('Aucun fichier sélectionné 2')
                #session['page'] = "accueil"
                return redirect(request.url)
            #on vérifie que c'est un zip
            if not allowed_file(file.filename):
                flash('Le fichier sélectionné doit être une archive zip.')
                #session['page'] = "accueil"
                return redirect(request.url)
            if file and allowed_file(file.filename):
                file.save(zipname)
                try:
                    feuilles = fsheets(zipname)
                except:
                    flash("Votre zip ne semble pas être une sauvegarde de classe Wims. Erreur de fichier ?")
                    return redirect(request.url)
    elif page == 'logout':
        cleanData(pseudo)
        session.pop('username', None)
        flash("Vos données ont été supprimées du serveur. Au revoir et à bientôt.")
        return redirect(request.url)
    elif page == 'result':
        feuille = int(request.form['feuille'])+1
        dtfct = data_factory(zipname,feuille,dirpath)
        if dtfct[0]=='error':
            flash(dtfct[1])
            return redirect(request.url)
        else:
            return dtfct
    return render_template('accueil.html', page=page, feuilles=feuilles)

application = app

#if __name__ == '__main__':
#    app.run(debug=True)