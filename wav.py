#! /usr/bin/env python3
# coding: utf8

from htm import *
from rtf import *
from zipfile import ZipFile
from LigneLog import *

feuille = 28
name = "analyse-feuille " + str(feuille)
fhtm = open(name + ".html", "w")
frtf = open(name + ".rtf", "w")


def crlist():
    """ Crée la liste des participants ayant travaillé dans la classe
    """
    with ZipFile('wims.zip') as myzip:
        names = myzip.namelist()
        liste = []
        for file in names:
            if '/score' in file and '.exam' not in file and 'supervisor' not in file:
                tmp = file.split('/')[-1]
                if tmp != '':
                    liste.append(tmp)
    return liste


def fname(username):
    """ Va chercher le nom et le prénom du participant
    """
    with ZipFile('wims.zip') as myzip:
        file = myzip.read('class/.users/' + username)
        file = file.decode('latin1').split('\n')
        for line in file:
            if 'lastname' in line:
                lastname = line.split('=')[1]
            elif 'firstname' in line:
                firstname = line.split('=')[1]
    return firstname, lastname


titre = "Visualisation de  l'activité des élèves sur la feuille  :" + \
    str(feuille)
beghtm(fhtm, titre)
begrtf(frtf, titre)

loginlist = crlist()

for login in loginlist:
	firstname, name = fname(login)
	with ZipFile('wims.zip') as myzip:
		content = myzip.read('class/score/' + login)
		content = content.decode('utf8').replace('  ', ' ')
		content = content.split('\n')
		content.pop()  # enl&egrave;ve le dernier &eacute;l&eacute;ment (une ligne vide)
	listelog = [" "] * 50  # va contenir les textes exo par exo
	listesession = [" "] * 50  # va contenir les num session exo par exo
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
			if(exo > len(listelog)):
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
				c = str(line.score) + " "
				c = c.replace(".0", " ")
				listedureesscores[exo] += dureescore
			listedurees[exo] += duree
			listelog[exo - 1] += colorhtm(color,c)
	dureetotale = 0
	for i in range(50):
		dureetotale += listedurees[i]
	htotale = dureetotale // 3600
	stotale = dureetotale % 3600
	mintotale = stotale // 60
	stotale = stotale % 60

	sdureetotale = 0
	for i in range(50):
		sdureetotale += listedureesscores[i]
	hstotale = sdureetotale // 3600
	sstotale = sdureetotale % 3600
	minstotale = sstotale // 60
	sstotale = sstotale % 60

	texte = emphhtm("Travail sur Wims : ") + "feuille n°" + str(feuille)
	parhtm(fhtm, texte)
	texte = emphhtm("Elève : ") + firstname + " " + name
	parhtm(fhtm, texte)
	texte = emphhtm("Durée approximative de travail : ") + str(htotale) + " h " + str(mintotale) + " min ... et sans doute plus de " + str(hstotale) + " h " + str(minstotale) + " min."
	parhtm(fhtm, texte)
	texte=emphhtm("Légende : ") + " Chaque tiret indique la visualisation d'un nouvel énoncé \
	(un tiret long indique une recherche de plus de 5 minutes et un point une recherche de moins d'une minute).<br />\
	Chaque nombre indique un score obtenu.<br />\
	La" + colorhtm("green"," couleur verte") + " indique que l'enregistrement des notes est désactivé.<br />\
	La" + colorhtm("red"," couleur rouge") + " indique que l'enregistrement des notes est activé."
	parhtm(fhtm, texte)
	for i in range(50):
		if(listelog[i] != " "):
			parhtm(fhtm,emphhtm(" Exercice n°" + str(i + 1)) + listelog[i])
	parhtm(fhtm,emphhtm("Commentaires : ") + "<hr>")


endrtf(frtf)
endhtm(fhtm)
fhtm.close()
frtf.close()
