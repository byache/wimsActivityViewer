#! /usr/bin/env python3
# coding: utf8
# ce fichier est le fichier principal (l'app)

import os
from flask import Flask, flash, request, redirect, url_for, render_template, session
from werkzeug.utils import secure_filename
from io import BytesIO
from data_factory import * #contient des fonctions enlevées d'ici pour ne pas surcharger...
from uuid import uuid4

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'zip'}

app = Flask(__name__)
app.secret_key = 'GZD9qr}3Q]9p7iW._5?s'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 #max size 10 Mo

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def main_function():
	# on regarde si c'est la première page qui est vue dans la session
	if 'pseudo' not in session :
		# si oui, on attribue un numéro aléatoire unique de session et on le stocke dans le cookie 'pseudo'
		pseudo = uuid4().hex
		session['pseudo'] = pseudo
		session['page'] = "accueil"
		
	#succession des vues : ["accueil","feuille","result"]
	pseudo = session['pseudo']
	page = session['page']
	if request.method == 'POST' and page == 'accueil':
		# check if the post request has the file part
		if 'file' not in request.files:
		    flash('Aucun fichier sélectionné')
		    return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('Aucun fichier sélectionné 2')
			return redirect(request.url)
		#on vérifie que c'est un zip
		if not allowed_file(file.filename):
			flash('Le fichier sélectionné doit être une archive zip.')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(pseudo+'.zip')
			filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			flash(filepath)
			file.save(filepath)
			session['page'] = "feuille"
			#return data_factory(BytesIO(file.read()),f)
	elif page == 'feuille':
		session['page'] = 'result'
	elif page == 'result':
		#feuille = int(request.form['feuille'])
		#filename = pseudo+'.zip'
		#filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		return data_factory('uploads/ff7c7e0dfe594124804e6bceed14513e.zip',28)
	#avant d'afficher la page, on recherche quelle sera la page suivante et on la met dans le cookie session
	#page2 = itineraire[(itineraire.index(page)+1)%3]
	#session['page']=page2
	flash(session)
	return render_template('accueil.html', page=page)

application = app
