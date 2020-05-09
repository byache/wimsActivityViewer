#! /usr/bin/env python3
# coding: utf8
#ce fichier contient des fonctions utilisées dans wav.py

from htm import *
from rtf import *
from zipfile import ZipFile
from classes import *
from flask import render_template

feuille = 28

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
			
	
		#données à envoyer à la vue pour affichage (on se limite à 50 exos)
		listsession=[[] for i in range(50)] #un élément par exo. Cet élément va contenir une liste de dates de sessions
		listdata=[[] for i in range(50)] #un élément par exo. Cet élément va contenir une liste de données à afficher
		
		ses=[" "]*50 #mémoire du numéro de la session en cours exo par exo
		dur=[0]*50 #tps de travail exo par exo
		durmin=[0]*50 #tps de travail aboutissant à un score 
		
		for numline in range(len(content)):
			line = LigneLog(content[numline])
			
			if(line.sheet == feuille):
				exo = line.exercise
				if(exo > len(listdata)): #il y avait plus de 50 exos dans la feuille mettre un message d'erreur sur la page ?
					print(
						"Attention : exercices non pris en compte car la taille de listelog se limite à " +
						len(listelog) +
						" exercices...")
						
				#calcul du temps de travail
				if numline + 1 < len(content):
					line2 = LigneLog(content[numline + 1])
					duree = 0
					#si la ligne d'après existe et a le même numéro de session, on comptabilise du temps de travail jusque là
					if line2.session == line.session:
						duree = int(line2.time - line.time)
				dureescore = 0
				#si l'élève a eu un score, on comptabilise du temps de travail aboutissant à un score
				if numline > 0 and line.type=='score' :
					line1 = LigneLog(content[numline - 1])
					if line1.session == line.session:
						dureescore = int(line.time - line1.time)


				if str(line.session) != str(ses[exo - 1]): #on a changé de session
					ses[exo - 1] = line.session 
					listdata[exo - 1].append({'date' : line.date ,	'heure' : line.timetext ,'data' : []}) #listdata[j] contient la liste des {date,heure de début,données d'activité} des sessions sur l'exo j+1
				color = "green"
				if(line.sc):
					color = "red" #couleur rouge si le score est activé, verte sinon
				c=" -" #tiret court
				if duree<60:
					c=" ·" #point si recherche de moins d'une minute
				if duree>300:
					c=" –" #tiret long si recherche de plus de 5 minutes
				if(line.type == "score"):
					c = str(int(line.score)) + " "
					durmin[exo-1] += dureescore 
				dur[exo-1] += duree 
				listdata[exo - 1][-1]['data'].append([color,c]) #les données d'activités sont une liste de couples "couleur,caractère / score"

		user.listdata = listdata
		dureetotale = 0
		for duree in dur:
			dureetotale += duree
		user.h = dureetotale // 3600
		stotale = dureetotale % 3600
		user.min = stotale // 60

		sdureetotale = 0
		for duree in durmin:
			sdureetotale += duree
		user.sh = sdureetotale // 3600
		sstotale = sdureetotale % 3600
		user.smin = sstotale // 60
		
	return render_template('resultat.html', feuille=feuille, data=data)

