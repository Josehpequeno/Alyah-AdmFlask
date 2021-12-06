from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from app import app, db

from dao import MangasDao

from models import Administrator


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


@app.route('/addUser', methods=['GET', 'POST'])
def addUser():
    if request.method == 'GET':
        return render_template('addUser.html')
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        adm = Administrator(name, email, password)
        check = Administrator.checkAdm(adm, name, email, password)
        if check != True:
            flash(check)
            return render_template('addUser.html', adm=adm, error=True)
        if confirm_password != password:
            flash('Passwords do not match')
            return render_template('addUser.html', adm=adm, error=True)
        flash('Administrator added successfully')
        return render_template('addUser.html', adm=adm, sucess=True)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signout')
def signout():
    pass
    # return render_template('template.html')
