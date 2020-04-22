#! /usr/bin/env python3
# coding: utf8

def beghtm(f,text):
    """ Insère le début du fichier html
    """
    f.write("<html><head><title>" + text + "</title></head><body>")


def endhtm(f):
    """ Insère la fin du fichier html
    """
    f.write("</body></html>")


def parhtm(f,text):
    """ Insère un paragraphe (html)
    """
    f.write("<p>" + accenthtm(text) + "</p>")


def tchtm():
    """tiret court html
    """
    return " &ndash;"


def tlhtm():
    """tiret long html
    """
    return " &mdash;"


def pthtm():
    """point html
    """
    return " &middot;"


def emphhtm(text):
    """ gras italique souligné
    """
    return "<b><u><i>" + text + "</i></u></b>"


def redhtm(text):
    """ en rouge (gras) au format html
    """
    return "<font color='red'><b>" + text + "</b></font>"


def greenhtm(text):
    """ en vert au format html
    """
    return "<font color='green'>" + text + "</font>"


def accenthtm(text):
    """gère les accents en html
    """
    res = text.replace('é', '&eacute;')
    res = res.replace('è', '&egrave;')
    res = res.replace('à', '&agrave;')
    return res

