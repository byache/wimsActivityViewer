#! /usr/bin/env python3
# coding: utf8
#ce fichier contient des fonctions utilisées dans datafactory.py

from zipfile import ZipFile
from flask import flash 


def indicateurs(listscores,req,sn,st):
    """calcule les indicateurs de l'exo si on a obtenu les scores listscores et que le nombre de points requis est req
    """
    n=int(req/10)
    i0=0
    for s in listscores:
        i0+=s
    if i0>req:
        i0=req
    i0=i0/req
    
    i1=0
    listdecr=sorted(listscores,reverse=True)
    m=n
    if len(listdecr)<n:
        m=len(listdecr)
    for num in range(m):
       i1+=listdecr[num]
    i1=i1/req
    
    i2=0
    if len(listdecr)>=n:
        i2=listdecr[n-1]/10
    
    q=0
    totalcoef=0
    t=len(listscores)
    for k in range(t):
        coef=0.85**(t-k-1)
        q+=listscores[k]*coef
        totalcoef+=coef
    if totalcoef!=0:
        q=q/totalcoef
        #si le nombre d'essais non terminés s n, est strictement 
        #supérieur à 5+2s t, où s t est le nombre d'essais terminés (avec une note), 
        #la note de qualité est multipliée par 2s t/(s n−4)<1. 
        if sn>5+2*st:
            q=q*2*st/(sn-4)
    return [i0,i1,i2,q]

def preparescore(feuille,file):
    with ZipFile(file) as myzip:
        weights = myzip.read('class/sheets/.weight')
        weights = weights.decode('utf8').split('\n')[feuille-1]
        weights = weights.split(' ') #on a une liste des coeff de pondération des exos de la feuille feuille
        requires = myzip.read('class/sheets/.require')
        requires = requires.decode('utf8').split('\n')[feuille-1]
        requires = requires.split(' ') #on a une liste des points requis pour chaque exo de la feuille feuille
    with ZipFile(file) as myzip:
        sev = myzip.read('class/sheets/.severity')
        sev = sev.decode('utf8').split('\n')
        maxi=int(sev[0]) #le nombre total de points sur lequel la note est calculée.
        try:
            sev = sev[feuille]
            sev = sev.split(' ') #on a une liste poids , règle de calcul (entre 0 et 5) , indicateur (entre 0 et 2)
            sev=[b for b in sev if b] #on enlève les éléments vides
        except:
            sev=[]
        if sev==[]:
            sev = [1,2,1]
            flash("Votre feuille n'avait pas de paramètre pour le calcul du score (peut-être est-ce une vieille feuille ?). Les paramètres choisis sont : poids : 1 ; règle de calcul : \"I*Q^0.3\" ; indicateur : I1 (moyenne des meilleurs scores à chaque exercice).")
        
        try:
            sev[0]=float(sev[0])
        except:
            sev[0]=1
            flash("Votre feuille n'avait pas de poids (peut-être est-ce une vieille feuille ?). Le poids a été mis à 1.")
        try:
            sev[1]=int(sev[1])
        except:
            sev[1]=2
            flash("Votre feuille n'avait pas de règle de calcul pour le score (peut-être est-ce une vieille feuille ?). La règle de calcul a été mise à \"I*Q^0.3\".")
        try:
            sev[2]=int(sev[2])
        except:
            sev[2]=1
            flash("Votre feuille n'avait pas de choix d'indicateur à utiliser (peut-être est-ce une vieille feuille ?). L'indicateur choisi est I1 (moyenne des meilleurs scores à chaque exercice).")
    return [weights, requires, maxi, sev]

def computescore(listscores,prepare,sn,st):
    """calcule la note à la feuille de travail avec les paramètres donnés dans prepare si on a eu les scores listscores aux exercices
    listscores et une liste de listes : une liste par exercice, regroupant les scores obtenus à cet exo
    la note est donnée sus la forme "7.5/10". C'est donc du string.
    """
    nbex=len(listscores) #nbre d'exercices
    weights,requires,maxi,sev=prepare
    I0,I1,I2,Q,sommecoef,sommecoefQ = 0,0,0,0,0,0
    for num in range(nbex):
        list = listscores[num]
        req = float(requires[num])
        ind = indicateurs(list,req,sn[num],st[num])
        if ind[3]<1: #qualité de l'exo inférieure à 1
            ind[0]=0
            ind[1]=0
            ind[2]=0
        elif ind[3]<2: #qualité de l'exo entre 1 et 2
            ind[0]=ind[0]/2
            ind[1]=ind[1]/2
            ind[2]=ind[2]/2
        coef = float(weights[num])*req
        coefQ = float(weights[num])*ind[0]
        sommecoef+=coef
        sommecoefQ+=coefQ
        I0 += ind[0]*coef
        I1 += ind[1]*coef
        I2 += ind[2]*coef
        Q += ind[3]*coefQ
    if sommecoef != 0:
        I0=I0/sommecoef
        I1=I1/sommecoef
        I2=I2/sommecoef
    if sommecoefQ!=0:
        Q=Q/sommecoefQ
    Q=Q/maxi #pour ramener Q entre 0 et 1

    indic = [I0,I1,I2]
    I = indic[sev[2]]
    regle = sev[1]
    note = 0
    if regle == 0:
        note = I
        if Q>I:
            note = Q
    elif regle==1:
        note = I
    elif regle == 2:
        note = I*Q**0.3
    elif regle == 3:
        note = I*Q**0.5
    elif regle == 4:
        note = I*Q
    elif regle == 5:
        note = I**2*Q
    elif regle == 6:
        note = (I*Q)**2
    note=note*maxi #pour mettre la note entre 0 et maxi
    note=round(note,2) #arrondi centième
    notetexte=str(note)+'/'+str(maxi)
    return notetexte

