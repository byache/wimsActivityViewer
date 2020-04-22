#! /usr/bin/env python3
# coding: utf8


class LigneLog:
    # chaque ligne de log devient un objet
    def __init__(self, lineraw):
        # ligne raw designe la ligne "brute"
        lineraw = lineraw + '\t'
        lineraw = lineraw.split('\t')
        self.sc = True
        if(lineraw[2] == "noscore"):
            self.sc = False
        self.IP = lineraw[1]
        lineraw = lineraw[0].split(' ')
        dateraw = lineraw[0].split('.')
        self.date = dateraw[0]
        timeraw = dateraw[1].split(':')
        self.time = int(timeraw[0]) * 3600 + \
            int(timeraw[1]) * 60 + int(timeraw[2])
        self.timetext = dateraw[1]
        self.session = lineraw[1]
        self.sheet = int(lineraw[2])
        self.exercise = int(lineraw[3])
        self.type = lineraw[4]
        self.score = 0
        if(lineraw[4] == "score"):
            self.score = float(lineraw[5])
