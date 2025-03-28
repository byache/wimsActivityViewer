#! /usr/bin/env python3
# coding: utf8

from time import mktime

# cette classe gère les données des lignes du fichier de log "scores"
#extrait de ce genre de fichier :
#20191215.19:17:52 RH225FD237 28  1 renew   109.0.207.75    181276269   noscore
#20191215.19:17:59 RH225FD237 28  1 score 0     109.0.207.75        noscore
#20191215.19:18:09 RH225FD237 28  1 new     109.0.207.75    181613962
#20191215.19:18:13 RH225FD237 28  1 score 10    109.0.207.75
class LigneLog:
	# chaque ligne de log devient un objet
	def __init__(self, lineraw):
		# ligne raw designe la ligne "brute"
		lineraw = lineraw + '\t'
		lineraw = lineraw.split('\t')
		lineraw=[x for x in lineraw if x] #pour enlever tout les éléments "falsy" du genre '' ou encore []

		self.sc = True
		if("noscore" in lineraw):
			self.sc = False
		#self.IP = lineraw[1] on n'enregistre pas l'ip par souci de confidentialité
		lineraw = lineraw[0].split(' ')
		lineraw=[x for x in lineraw if x] #pour enlever tout les éléments "falsy" du genre '' ou encore []

		dateraw = lineraw[0].split('.')
		dateraw2 = dateraw[0]
		self.date = dateraw2[6:8] + "/" + dateraw2[4:6] + \
					"/" + dateraw2[0:4]
		self.timetext = dateraw[1]
		timeraw = dateraw[1].split(':')
		structime = int(dateraw2[0:4]),int(dateraw2[4:6]),int(dateraw2[6:8]),int(timeraw[0]),int(timeraw[1]),int(timeraw[2]),0,1,-1
		self.time = mktime(structime)
		self.session = lineraw[1]
		self.sheet = int(lineraw[2])
		
		self.exercise = int(lineraw[3])
		self.type = lineraw[4]
		self.score = 0
		if(lineraw[4] == "score"):
			self.score = float(lineraw[5])

#cette classe gère les données des examens (dossier "noscores")
#extrait de ce genre de fichier :
#E20241014.19:23:33 BG094BEA8D  3  3 new  	2.9.112.193	1944412905		6.9
#E20241014.19:25:34 BG094BEA8D  3  3 score 10  	2.9.112.193		
#E20241014.19:25:53 BG094BEA8D  3  2 new  	2.9.112.193	1944706684		25.1
#E20241014.19:31:49 BG094BEA8D  3  2 score 0  	2.9.112.193		
class LigneLogExam:
	# chaque ligne de log devient un objet
	def __init__(self, lineraw):
		# ligne raw designe la ligne "brute"
		lineraw = lineraw.split()
		lineraw=[x for x in lineraw if x] #pour enlever tout les éléments "falsy" du genre '' ou encore []
		#self.IP = lineraw[1] on n'enregistre pas l'ip par souci de confidentialité
		lineraw=[x for x in lineraw if x] #pour enlever tout les éléments "falsy" du genre '' ou encore []
		dateraw = lineraw[0].split('.')
		dateraw2 = dateraw[0][1:] #pour enlever le premier caractère qui est un "E"
		self.date = dateraw2[6:8] + "/" + dateraw2[4:6] + \
					"/" + dateraw2[0:4]
		self.timetext = dateraw[1]
		timeraw = dateraw[1].split(':')
		structime = int(dateraw2[0:4]),int(dateraw2[4:6]),int(dateraw2[6:8]),int(timeraw[0]),int(timeraw[1]),int(timeraw[2]),0,1,-1
		self.time = mktime(structime)
		self.session = lineraw[1]
		self.exam = int(lineraw[2])
		
		self.exercise = int(lineraw[3])
		self.type = lineraw[4]
		self.ref =''
		if(lineraw[4] == "new"):
			self.ref = str(lineraw[7])
		self.score = 0
		if(lineraw[4] == "score"):
			self.score = float(lineraw[5])

# cette classe gère les données des utilisateurs
class User:
	# chaque ligne de log devient un objet
	def __init__(self):
		self.login = ''
		self.firstname = ''
		self.lastname = ''
		self.h = 0
		self.min = 0
		self.sh = 0
		self.smin = 0
		self.note = 0
		self.listdata = []
