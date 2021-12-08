from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from app import app, db

from dao import MangasDao

from models import Administrator, Mangas


@app.route('/')  # definição de uma rota
def home():
    manga_dao = MangasDao(db)
    mangas = manga_dao.getAllMangas()
    return render_template('home.html', mangas=mangas)
    # tem que estar na pasta de templates


@app.route('/mangas/<string:option>')
def mangas(option):
    return render_template('mangas.html', option=option)

@app.route('/mangasCreate', methods=['POST'])
def mangasCreate():
    name = request.form['name']
    author = request.form['author_name']
    cover = request.form['cover']
    description = request.form['description']

    manga = Mangas(name, description, author, cover)
    
    flash("Manga Successfully Added")
    # return render_template('mangas.html', option='Create', error=True)
    return render_template('mangas.html', option='Create', sucess=True)

@app.route('/mangasUpdate', methods=['POST'])
def mangasUpdate():
    name = request.form['name']
    author = request.form['author_name']
    cover = request.form['cover']
    description = request.form['description']
    
    manga = Mangas(name, description, author, cover)

    flash("Manga Updated Successfully")
    # return render_template('mangas.html', option='Create', error=True)
    return render_template('mangas.html', option='Update', sucess=True)

@app.route('/mangasDelete', methods=['POST'])
def mangasDelete():
    name = request.form['name']
    author = request.form['author_name']
    cover = request.form['cover']
    description = request.form['description']
    
    manga = Mangas(name, description, author, cover)

    flash("Manga Successfully Deleted")
    # return render_template('mangas.html', option='Create', error=True)
    return render_template('mangas.html', option='Delete', sucess=True)


@app.route('/chapters/<string:option>')
def chapters(option):
    return render_template('chapters.html', option=option)

@app.route('/chaptersCreate', methods=['POST'])
def chaptersCreate():
    name = request.form['name']
    author = request.form['author_name']
    cover = request.form['cover']
    description = request.form['description']

    chapters = Mangas(name, description, author, cover)
    
    flash("Chapters Successfully Added")
    # return render_template('mangas.html', option='Create', error=True)
    return render_template('chapters.html', option='Create', sucess=True)

@app.route('/chaptersUpdate', methods=['POST'])
def chaptersUpdate():
    name = request.form['name']
    author = request.form['author_name']
    cover = request.form['cover']
    description = request.form['description']
    
    chapters = Mangas(name, description, author, cover)

    flash("Chapters Updated Successfully")
    # return render_template('mangas.html', option='Create', error=True)
    return render_template('chapters.html', option='Update', sucess=True)

@app.route('/chaptersDelete', methods=['POST'])
def chaptersDelete():
    name = request.form['name']
    author = request.form['author_name']
    cover = request.form['cover']
    description = request.form['description']
    
    chapters = Mangas(name, description, author, cover)

    flash("Manga Successfully Deleted")
    # return render_template('mangas.html', option='Create', error=True)
    return render_template('chapters.html', option='Delete', sucess=True)



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

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('500.html'), 404