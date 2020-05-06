#! /usr/bin/env python3
# coding: utf8
#ce fichier contient des fonctions utilisées dans wav.py

from htm import *
from rtf import *
from zipfile import ZipFile
from classes import *
from flask import render_template

feuille = 28
name = "analyse-feuille " + str(feuille)
fhtm = open(name + ".html", "w")
frtf = open(name + ".rtf", "w")

from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('wimsActivityViewer', 'templates'),
    autoescape=select_autoescape(['html'])
)


def crlist(file):
    """ Crée la liste des participants ayant travaillé dans la classe
    """
    with ZipFile(file) as myzip:
        names = myzip.namelist()
        liste = []
        for file in names:
            if '/score' in file and '.exam' not in file and 'supervisor' not in file:
                tmp = file.split('/')[-1]
                if tmp != '':
                    liste.append(tmp)
    return liste


def fname(file,username):
    """ Va chercher le nom et le prénom du participant
    """
    with ZipFile(file) as myzip:
        file2 = myzip.read('class/.users/' + username)
        file2 = file2.decode('latin1').split('\n')
        for line in file2:
            if 'lastname' in line:
                lastname = line.split('=')[1]
            elif 'firstname' in line:
                firstname = line.split('=')[1]
    return firstname, lastname

#fonction principale, qui génère un fichier odt et le contenu de la vue html
def data_factory(file,feuille):  #file : le fichier .zip contenant l'archive de la classe wims ; feuille : un integer contenant le numéro de la feuille wims à regarder
	loginlist = crlist(file)
	data = [User() for login in loginlist]
	
	for i in range(len(data)):
		login = loginlist[i]
		user = data[i]
		user.firstname, user.lastname = fname(file,login)
	
		with ZipFile(file) as myzip:
			content = myzip.read('class/score/' + login)
		content = content.decode('utf8').replace('  ', ' ')
		content = content.split('\n')
		content.pop()  # enlève le dernier élément (une ligne vide)
			
		listelog = [" "] * 50  # va contenir les textes exo par exo
		listesession = [" "] * 50  # va contenir les num de session exo par exo
		listedurees = [0] * 50  # va contenir les temps de travail exo par exo
		# va contenir les temps de travail des lignes "score" exo par exo
		listedureesscores = [0] * 50
		for numline in range(len(content)):
			line = LigneLog(content[numline])
			if numline + 1 < len(content):
				line2 = LigneLog(content[numline + 1])
				duree = 0
				if line2.session == line.session:
					duree = int(line2.time - line.time)
			dureescore = 0
			if numline > 0:
				line1 = LigneLog(content[numline - 1])
				if line1.session == line.session:
					dureescore = int(line.time - line1.time)
			if(line.sheet == feuille):
				exo = line.exercise
				if(exo > len(listelog)): #mettre un message d'erreur sur la page ?
					print(
						"Attention : exercices non pris en compte car la taille de listelog se limite à " +
						len(listelog) +
						" exercices...")

				if str(line.session) != str(listesession[exo - 1]):
					listesession[exo - 1] = line.session
					listelog[exo - 1] += "<br />Le " + line.date + " à partir de " + \
							line.timetext + " : "
				color = "green"
				if(line.sc):
					color = "red"
				c=" -" #tiret court
				if duree<60:
					c=" ·" #point si recherche de moins d'une minute
				if duree>300:
					c=" –" #tiret long si recherche de plus de 5 minutes
				if(line.type == "score"):
					c = str(int(line.score)) + " "
					listedureesscores[exo] += dureescore
				listedurees[exo] += duree
				listelog[exo - 1] += colorhtm(color,c)

		user.listelog = listelog
		dureetotale = 0
		for i in range(50):
			dureetotale += listedurees[i]
		user.h = dureetotale // 3600
		stotale = dureetotale % 3600
		user.min = stotale // 60

		sdureetotale = 0
		for i in range(50):
			sdureetotale += listedureesscores[i]
		user.sh = sdureetotale // 3600
		sstotale = sdureetotale % 3600
		user.smin = sstotale // 60
		
	return render_template('resultat.html', feuille=feuille, data=data)

