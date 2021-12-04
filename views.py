from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from app import app, db

from dao import MangasDao

@app.route('/')  # definição de uma rota
def home():
    manga_dao = MangasDao(db)
    mangas = manga_dao.getAllMangas()
    return render_template('home.html', mangas=mangas)
    # tem que estar na pasta de templates


@app.route('/mangas')
def mangas():
    pass
    # return render_template('mangas.html')

@app.route('/manga/<name>')
def manga(name):
    pass
    # return render_template('template.html')


@app.route('/chapters')
def chapters():
    pass
    # return render_template('template.html')


@app.route('/addUser')
def addUser():
    pass
    # return render_template('template.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signout')
def signout():
    pass
    # return render_template('template.html')
