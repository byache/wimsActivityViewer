#! /usr/bin/env python3
# coding: utf8

def beghtm(f,text):
    """ Insère le début du fichier html
    """
    f.write("<html>\n<head>\n<title>\n" + accenthtm(text) + "\n</title>\n</head>\n<body>\n")


def endhtm(f):
    """ Insère la fin du fichier html
    """
    f.write("</body>\n</html>")


def parhtm(f,text):
    """ Insère un paragraphe (html)
    """
    f.write("<p>\n" + accenthtm(text) + "\n</p>\n")


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
    return "<b><i>" + text + "</i></b>"


def colorhtm(color,text):
	""" en rouge (gras) ou en vert (ou autre) au format html
	"""
	b1 = ""
	b2 = ""
	col = color
	if color == "vert":
		col = "green"
	if color == "rouge" or color == "red":
		col = "red"
		b1 = "<b>"
		b2 = "</b>"
	return "<font color='" + col + "'>" + b1 + text + b2 + "</font>"


def accenthtm(text):
    """gère les accents en html
    """
    res = text.replace('é', '&eacute;')
    res = res.replace('è', '&egrave;')
    res = res.replace('à', '&agrave;')
    res = res.replace('°', '&deg;')
    return res

