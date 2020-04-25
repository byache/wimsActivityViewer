#! /usr/bin/env python3
# coding: utf8


from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')
def accueil():
    return render_template('accueil.html')

