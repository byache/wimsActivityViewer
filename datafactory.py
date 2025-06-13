#! /usr/bin/env python3
# coding: utf8
#ce fichier contient des fonctions utilisées dans wav.py

from zipfile import ZipFile
from classes import *
from flask import render_template,flash,redirect,request
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties, FontFace
from odf.text import H, P, Span
from odf.office import FontFaceDecls
from notes import *
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import os.path

env = Environment(
	loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__))
)


def crlist(file):
	""" Crée la liste des participants de la classe
	"""
	with ZipFile(file) as myzip:
		file2 = myzip.read('class/.userlist')
		file2 = file2.decode('latin1').split('\n')
		data = []
		for line in file2:
			if len(line)>2: 
				line = line.split(',')
				user = User()
				user.lastname = line[0].replace(':','')
				user.firstname = line[1]
				user.login = line[2]
				data.append(user)
	return data

	
def fsheets(file):
	""" Va chercher la liste des titres des feuilles et des examens
	structure : [listefeuilles,listeexamens]
	avec listefeuille=[liste de couples[Ei (ou Si),"titre exam ou feuille i"]]
	"""
	with ZipFile(file) as myzip:
		file2 = myzip.read('class/sheets/.sheets')
		file2 = file2.decode('latin1').split('\n:')
		res = [list(),list()] #première liste pour les feuilles et 2e pour les examens
		i=0
		for sh in file2:
			if len(sh)>2 :
				titre = 'feuille&nbsp;'+str(i)+'&nbsp;:&nbsp;'+sh.split('\n')[2]
				res[0].append(["S"+str(i),titre])
			i+=1
		file2 = myzip.read('class/exams/.exams')
		file2 = file2.decode('latin1').split('\n:')
		i=0
		for sh in file2:
			if len(sh)>2 :
				titre = 'examen&nbsp;'+str(i)+'&nbsp;:&nbsp;'+sh.split('\n')[3]
				res[1].append(["E"+str(i),titre])
			i+=1
	return res

def cntnbex(file,typ,num):
	""" Va chercher le nombre d'exercice de l'examen ou de la feuille
	typ : E pour examen ou S pour feuille
	num : numéro de l'examen ou de la feuille
	"""
	if typ == 'E':
		chemin='class/exams/.exam'+str(num-1)
	else :
		chemin='class/sheets/.sheet'+str(num-1)
	with ZipFile(file) as myzip:
		file2 = myzip.read(chemin)
		file2 = file2.decode('latin1').split('\n:')
		return len([sh for sh in file2 if sh != ''])


def createodt(file,data,feuille,nom,dirpath):

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
	pb.addElement(ParagraphProperties(breakafter="page")) #mettre breakafter ?
	textdoc.automaticstyles.addElement(pb)
	# Text
	p = P()
	part = Span(stylename = b, text="Mode d'emploi pour le prof : ")
	p.addElement(part)
	textdoc.text.addElement(p)
	p = P()
	part = Span(text="Il y a une page par élève.")
	p.addElement(part)
	textdoc.text.addElement(p)
	p = P()
	part = Span(text="Compléter le bas de chaque page par un commentaire, par exemple sur l'efficacité des méthodes de travail de l'élève.")
	p.addElement(part)
	textdoc.text.addElement(p)
	p = P()
	part = Span(text="Imprimer en deux pages par feuilles et faire un rendu à la classe.")
	p.addElement(part)
	textdoc.text.addElement(p)
	
	p = P()
	textdoc.text.addElement(p)
	
	p = P(stylename=pb)
	textdoc.text.addElement(p)
	
	for user in data:
		p = P()
		part = Span(stylename=b, text = "Bilan du travail sur Wims : ")
		p.addElement(part)
		part = Span(text = nom)
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
		part = Span(text = str(user.note))
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
		p = P(text="Une lettre 'a' indique la consultation d'un indication.")
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

		p = P()
		textdoc.text.addElement(p)
		
		p = P()
		part = Span(stylename = b, text="Commentaires : ")
		p.addElement(part)
		textdoc.text.addElement(p)
		
		p = P()
		textdoc.text.addElement(p)
		
		p = P(stylename=pb)
		textdoc.text.addElement(p)
	titre = 'WimsActivityViewer_feuille_'+str(feuille)+'.odt'
	titre = os.path.join(dirpath,titre)
	textdoc.save(titre)
	return titre

#fonction principale, qui lit les données brutes, re-calcule la note de wims, génère un fichier odt et le contenu de la vue html
def data_factory(file,feuille,dirpath):  
	#file : le fichier .zip contenant l'archive de la classe wims ; feuille : une liste contenant la référence de la feuille ou des examens à regarder
	try:
		data = crlist(file) #liste des participants
	except:
		return 'error',"Vous devez renvoyer l'archive de votre classe car elle a été supprimée du serveur."

	listenoms=fsheets(file)
	#liste des premiers caractères pour voir s'il y a des E ou des S
	EorS=[ item[0] for item in feuille]
	#liste des numéros des examens ou feuilles :
	feuille=[ int(item[1:]) for item in feuille]
	#erreur si plusieurs feuilles cochées ou si feuilles et examens cochés simultanément
	if 'E' in EorS and 'S' in EorS :
		flash('Attention : vous ne pouvez pas mélanger des feuilles et des examens. Vous ne pouvez cocher qu\'une seule feuille ou alors un ou plusieurs examens.')
		page='accueil.html'
	elif 'S' in EorS and len(EorS)>1 :
		flash('Attention : vous ne pouvez pas cocher plusieurs feuilles.')
		page='accueil.html'
	#s'il faut analyser un examen
	elif 'E' in EorS :
		page='resultatexam.html'
		examen=feuille
		for i in range(len(data)):
			user = data[i]
			login = user.login
			tempsmini=0 #va contenir la somme des duree entre new et score
			tempsmaxi=0 #va contenir la somme des durées des sessions
			with ZipFile(file) as myzip:
				try:
					content = myzip.read('class/noscore/' + login).decode('utf8').replace('  ', ' ').split('\n')
					content.pop()  # enlève le dernier élément (une ligne vide) --> à vérifier
				except:
					content = []
			
			#données à envoyer à la vue pour affichage (on se limite à 50 sessions d'examen et à 50 exos par examen)
			nbses = 50 #(nombre de sessions max prises en compte pour cet examen) --> à affiner en récupérant le vrai nombre de sessions ?
			listsession=[[] for i in range(nbses)] #un élément par session. Cet élément va contenir une liste "nom,date,heure de sessions"
			note=0 # va contenir la meilleure note
			ses=" " #mémoire du numéro de la session en cours
			j=-1 #compteur des sessions
			debses=0 #pour l'heure de debut de session
			c="" #c va contenir un symbole montrant le temps de travail
			ref="" #va contenir la référence de l'exo
			for numline in range(len(content)):
				line = LigneLogExam(content[numline])
				if(line.exam in examen):
					exo = line.exercise
					if(exo > len(listsession)): #il y avait plus de 50 exos dans la feuille mettre un message d'erreur sur la page ?
						print(
							"Attention : exercices non pris en compte car le nombre maximum se limite à " +
							len(listsession) +
							" exercices...")

					if str(line.session) != str(ses): #on a changé de session
						j+=1
						ses = line.session 
						debses=line.time
						totalnoteses=0 #total des notes (IL FAUDRA PR>ENDRE EN COMPTE LES COEFF PLUS> TARD...)
						nbex=cntnbex(file,'E',line.exam+1)
						totalcoeffses=nbex #total des coeff (POUR LE MOMENT TOUJOURS DES 1...)
					
						listsession[j].append({'date' : line.date ,  'heure' : line.timetext ,'data' :[""]*(nbex),'note' : 0, 'nom' : listenoms[1][line.exam-1][1]}) 
						#listsession[j] contient la liste des {date,heure de début,liste des références des exos,données d'activité} des sessions sur la session j

					if(line.type == "new"):
						ref=line.ref
						if numline<len(content)-1:
							line2 = LigneLogExam(content[numline + 1])
							if str(line2.session)==str(ses):
								duree=int(line2.time - line.time)
								tempsmini+=duree
								c="·"*int(duree/60) #un point par minute
								c+=" X, "
								listsession[j][-1]['data'][line.exercise-1]=["("+str(ref)+")",c] #les données d'activités sont une liste de couples "reference, durée"
					if(line.type == "score"):
						c=c.replace("X",str(int(line.score)))
						totalnoteses+=line.score
						listsession[j][-1]['data'][line.exercise-1]=["("+str(ref)+")",c] #les données d'activités sont une liste de couples "couleur,caractère / score"
					if numline<len(content)-1:
						line2 = LigneLogExam(content[numline + 1])
						if str(line2.session) != str(ses): #on va changer de session à la requête suivante : il faut finaliser la duree et la note de cette session
							dureeses=int(line.time-debses)
							tempsmaxi+=dureeses
							noteses=int(totalnoteses*10/totalcoeffses)/10 #arrondie au dixième
							if noteses>note:
								note=noteses
							listsession[j][-1]['note']=noteses 
					else : #on est à la dernière requête
						dureeses=int(line.time-debses)
						tempsmaxi+=dureeses	
						#on enregistre la note de la session
						noteses=int(totalnoteses*10/totalcoeffses)/10 #arrondie au dixième
						if noteses>note:
							note=noteses
						listsession[j][-1]['note']=noteses 
							
			user.listdata = listsession
			user.h = tempsmaxi // 3600
			stotale = tempsmaxi % 3600
			user.min = stotale // 60
			user.sh = tempsmini // 3600
			stotale = tempsmini % 3600
			user.smin = stotale // 60
			user.note=note	

	else :
		#LA SUITE EST A RELIRE ET MODIFIER !!!
		page='resultat.html'
		flash('Bug pas encore corrigé : les notes de cette appli sont légèrement différentes (un peu supérieures) à celles de Wims')
		#s'il faut analyser un examen ou une feuille
		#feuille est le numéro de la feuille
		feuille=feuille.split(':')[1]
		feuille=int(feuille.replace('feuille','').replace('&nbsp;',''))
		prepare = preparescore(feuille,file)
		nbex = len(prepare[0])
		for i in range(len(data)):
			user = data[i]
			login = user.login
			with ZipFile(file) as myzip:
				try:
					content = myzip.read('class/score/' + login).decode('utf8').replace('  ', ' ').split('\n')
					content.pop()  # enlève le dernier élément (une ligne vide)
				except:
					content = []
			
	
			#données à envoyer à la vue pour affichage (on se limite à 50 exos)
			listsession=[[] for i in range(nbex)] #un élément par exo. Cet élément va contenir une liste de dates de sessions
			listdata=[[] for i in range(nbex)] #un élément par exo. Cet élément va contenir une liste de données à afficher
			listscores=[[] for i in range(nbex)] #un élément par exo. Cet élément va contenir la liste des scores obtenus à cet exo, dans l'ordre
			listscoresnote=[[] for i in range(nbex)] #un élément par exo. Cet élément va contenir la liste des scores à prendre en compte pour la note
			
			ses=[" "]*nbex #mémoire du numéro de la session en cours exo par exo
			dur=[0]*nbex #tps de travail exo par exo
			durmin=[0]*nbex #tps de travail aboutissant à un score 
			
			#st : nombre d'essais terminés de l'exos (aboutissant à une note)
			#sn : nombre d'essais total(nombre de génération d'énoncés)
			st=[0]*nbex
			sn=[0]*nbex
			
			for numline in range(len(content)):
				line = LigneLog(content[numline])
				if(line.sheet == feuille):
					exo = line.exercise
					if(exo > len(listdata)): #il y avait plus de 50 exos dans la feuille mettre un message d'erreur sur la page ?
						print(
							"Attention : exercices non pris en compte car le nombre maximum se limite à " +
							len(listdata) +
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
						listdata[exo - 1].append({'date' : line.date ,  'heure' : line.timetext ,'data' : []}) #listdata[j] contient le dictionnaire {date,heure de début,données d'activité} des sessions sur l'exo j+1
					color = "green"
					if(line.sc):
						color = "red" #couleur rouge si le score est activé, verte sinon
					c=" -" #tiret court
					if 'hint' in line.type:
						c=" a"
					elif 'rafale' in line.type:
						c=" rafale"
					elif duree<60:
						c=" ·" #point si recherche de moins d'une minute
					elif duree>300:
						c=" –" #tiret long si recherche de plus de 5 minutes
					if 'new' in line.type and line.sc:
						sn[exo-1]+=1
					if(line.type == "score"):
						
						c = " "+str(int(line.score)) + " "
						listscores[exo-1] += [line.score]
						if (line.sc):
							st[exo-1]+=1
							listscoresnote[exo-1] += [line.score]
						durmin[exo-1] += dureescore 
					dur[exo-1] += duree 
					listdata[exo - 1][-1]['data'].append([color,c]) #les données d'activités sont une liste de couples "couleur,caractère / score"

			#listsession = [x for x in listsession if x] #permet d'enlever tous les éléments vides []...
			#listdata = [x for x in listdata if x] #permet d'enlever tous les éléments vides []...
			#listscores = [x for x in listscores if x] #permet d'enlever tous les éléments vides []...
			
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
			
			user.note=computescore(listscoresnote,prepare,sn,st)
	
	if 'S' in EorS :
		nom = 'la feuille n°'+str(EorS)
	else :
		if len(EorS)==1 :
			nom = "l'examen n°"+str(feuille[0])
		else:
			nom = "les examens numéros : "+str(feuille)
	#lien = createodt(file,data,feuille,nom,dirpath)
	lien='ok'
	return render_template(page, feuille=feuille, data=data, lien=lien, nom=nom)

