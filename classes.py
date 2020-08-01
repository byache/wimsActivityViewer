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



# cette classe gère les données des utilisateurs
class User:
    # chaque ligne de log devient un objet
    def __init__(self):
        self.firstname = ''
        self.lastname = ''
        self.h = 0
        self.min = 0
        self.sh = 0
        self.smin = 0
        self.note = 0
        self.listdata = []
