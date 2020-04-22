#! /usr/bin/env python3
# coding: utf8


def begrtf(f, text):
    """ Insère dans f le début du fichier rtf
    """
    f.write(
        "{\\rtf1\\ansi\\n{\\fonttbl\\n  {\\f0\\fnil\\fcharset0\\fprq0\\fttruetype Helvetica;}}\\n")
    f.write("{\\colortbl ;  \\red0\\green128\\blue0;  \\red255\\green0\\blue0;  }\\n")
    f.write("{\\f0\\fs20 " + accentrtf(text) + "}\\n\\par\\n")


def endrtf(f):
    """ Insère dans f la fin du fichier rtf
    """
    f.write("\\n}")


def begpartrtf(f):
    """ Insère dans f le début de la partie consacrée à un participant (rtf)
    """


def endpartrtf(f):
    """ Insère dans f la fin de la partie consacrée à un participant (rtf)
    """


def sautpagertf():
    """insère un saut de page rtf
    """
    return '\\par \\pard\\plain \\s0\\widctlpar\\hyphpar0\\cf0\\kerning1\\dbch\\af5\\langfe2052\\dbch\\af6\\afs24\\alang1081\\loch\\f3\\hich\\af3\\fs24\\lang1036\\pagebb'


def redrtf(text):
    """ en rouge (gras) au format rtf
    """
    return "{\\cf2{\\b" + text + "}}"


def greenrtf(text):
    """ en vert au format rtf
    """
    return "{\\cf1" + text + "}"


def accentrtf(text):
    """gère les accents en rtf
    """
    res = text.replace('é', "\\'e9")
    res = res.replace('è', "\\'e8")
    res = res.replace('à', "\\'e9")
    return res
