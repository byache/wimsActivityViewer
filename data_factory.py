#! /usr/bin/env python3
# coding: utf8
#ce fichier contient des fonctions utilisées dans wav.py

from htm import *
from rtf import *
from zipfile import ZipFile
from classes import *
from flask import render_template

feuille = 28

from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties, FontFace
from odf.text import H, P, Span
from odf.office import FontFaceDecls

from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import os.path

env = Environment(
    loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__))
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

def fsheet(file,feuille):
    """ Va chercher le titre de la feuille numéro feuille
    """
    with ZipFile(file) as myzip:
        file2 = myzip.read('class/sheets/.sheets')
        file2 = file2.decode('latin1').split(':')
        file3 = file2[feuille+1].split('\n')
        titre = file3[2]
    return titre

def createodt(file,data):

	textdoc = OpenDocumentText()
	textdoc.fontfacedecls.addElement(FontFace(name="Arial",fontfamily="Arial",fontfamilygeneric="swiss",fontpitch="variable"))
	# Styles
	s = textdoc.styles
	#style normal   ---> faire plutôt un style par défaut en justilié taille 16...
	StandardStyle = Style(name="Standard", family="paragraph")
	StandardStyle.addElement(TextProperties(fontsize="16"))
	s.addElement(StandardStyle)
	# bold style
	b = Style(name="b", family="text", parentstylename='Standard')
	boldprop = TextProperties(fontweight="bold")
	b.addElement(boldprop)
	textdoc.automaticstyles.addElement(b)
	# red style
	r = Style(name="r", family="text", parentstylename='Standard')
	redprop = TextProperties(fontweight="bold", color="#FF0000")
	r.addElement(redprop)
	textdoc.automaticstyles.addElement(r)
	# green style
	g = Style(name="g", family="text", parentstylename='Standard')
	greenprop = TextProperties(color="#008000")
	g.addElement(greenprop)
	textdoc.automaticstyles.addElement(g)
	# Create a style for the paragraph with page-break
	pb = Style(name="pb", parentstylename="Standard", family="paragraph")
	pb.addElement(ParagraphProperties(breakbefore="page")) #mettre breakafter ?
	textdoc.automaticstyles.addElement(pb)
	# Text
	titre = 'WimsActivityViewer feuille '+str(feuille)
	for user in data:
		p = P()
		part = Span(stylename=b, text = "Bilan du travail sur Wims : ")
		p.addElement(part)
		part = Span(text = "feuille n°"+str(feuille)+" ("+fsheet(file,feuille)+")")
		p.addElement(part)		
		textdoc.text.addElement(p)
		
		p = P()
		textdoc.text.addElement(p)

		p = P()
		part = Span(stylename = b, text="Élève : ")
		p.addElement(part)
		part = Span(text = user.firstname+" "+user.lastname)
		p.addElement(part)
		textdoc.text.addElement(p)
		
		p = P()
		textdoc.text.addElement(p)
		
		p = P()
		part = Span(stylename = b, text="Note : ")
		p.addElement(part)
		part = Span(text = str(user.note)+" / 10")
		p.addElement(part)
		textdoc.text.addElement(p)
		
		p = P()
		textdoc.text.addElement(p)
		
		p = P()
		part = Span(stylename = b, text="Durée approximative de travail : ")
		p.addElement(part)
		part = Span(text = str(user.h)+" h "+str(user.min)+" min (sans doute plus que " + str(user.sh)+" h "+str(user.smin)+" min)")
		p.addElement(part)
		textdoc.text.addElement(p)
		
		p = P()
		textdoc.text.addElement(p)
		
		p = P()
		part = Span(stylename = b, text="Légende : ")
		p.addElement(part)
		p = P(text="Chaque tiret indique la visualisation d'un nouvel énoncé (un tiret long indique une recherche de plus de 5 minutes et un point une recherche de moins d'une minute).")
		textdoc.text.addElement(p)
		p = P(text="Chaque nombre indique un score obtenu.")
		textdoc.text.addElement(p)
		p = P(text="La ")
		part = Span(stylename=g, text = "couleur verte ")
		p.addElement(part)
		part = Span(text="indique que l'enregistrement des notes est désactivé.")
		p.addElement(part)
		textdoc.text.addElement(p)
		p = P(text="La ")
		part = Span(stylename=r, text = "couleur rouge ")
		p.addElement(part)
		part = Span(text="indique que l'enregistrement des notes est activé.")
		p.addElement(part)
		textdoc.text.addElement(p)
		
		p = P()
		textdoc.text.addElement(p)
		
		for i in range(len(user.listdata)):
			if len(user.listdata[i]) > 0 :
				p = P()
				part = Span(stylename = b, text="Exercice n° : "+str(i+1))
				p.addElement(part)
				textdoc.text.addElement(p)
				
				for dict in user.listdata[i]:
					p = P()
					part = Span(text="le "+dict['date'] + " à partir de " + dict['heure'] + " : ")
					p.addElement(part)
					for data in dict['data']:
						part = Span(stylename = data[0][0], text=data[1])
						p.addElement(part)
					textdoc.text.addElement(p)

		
		p = P(stylename=pb,text=u'Second paragraph')
		textdoc.text.addElement(p)
	textdoc.save(titre+".odt")

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
		
		createodt(file,data)
		
	return render_template('resultat.html', feuille=feuille, data=data)

