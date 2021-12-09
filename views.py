from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from app import app, db
from dao import MangasDao, AdministratorDao
from models import Administrator, Mangas
import hashlib


@app.route('/')  # definição de uma rota
def home():
    manga_dao = MangasDao(db)
    mangas = manga_dao.getAllMangas()
    try:
        user = session['USER']
    except Exception as error:
        user = None
    return render_template('home.html', mangas=mangas, user=user)
    # tem que estar na pasta de templates


@app.route('/mangas/<string:option>')
def mangas(option):
    try:
        user = session['USER']
    except Exception as error:
        return redirect(url_for('login'))
    return render_template('mangas.html', option=option, user=user)


@app.route('/mangasCreate', methods=['POST'])
def mangasCreate():
    try:
        user = session['USER']
    except Exception as error:
        return redirect(url_for('login'))
    name = request.form['name']
    author = request.form['author_name']
    cover = request.form['cover']
    description = request.form['description']

    manga = Mangas(name, description, author, cover)

    flash("Manga Successfully Added")
    # return render_template('mangas.html', option='Create', error=True)
    return render_template('mangas.html', option='Create', sucess=True, user=user)


@app.route('/mangasUpdate', methods=['POST'])
def mangasUpdate():
    try:
        user = session['USER']
    except Exception as error:
        return redirect(url_for('login'))
    name = request.form['name']
    author = request.form['author_name']
    cover = request.form['cover']
    description = request.form['description']

    manga = Mangas(name, description, author, cover)

    flash("Manga Updated Successfully")
    # return render_template('mangas.html', option='Create', error=True)
    return render_template('mangas.html', option='Update', sucess=True, user=user)


@app.route('/mangasDelete', methods=['POST'])
def mangasDelete():
    try:
        user = session['USER']
    except Exception as error:
        return redirect(url_for('login'))
    name = request.form['name']
    author = request.form['author_name']
    cover = request.form['cover']
    description = request.form['description']

    manga = Mangas(name, description, author, cover)

    flash("Manga Successfully Deleted")
    # return render_template('mangas.html', option='Create', error=True)
    return render_template('mangas.html', option='Delete', sucess=True, user=user)


@app.route('/chapters/<string:option>')
def chapters(option):
    try:
        user = session['USER']
    except Exception as error:
        return redirect(url_for('login'))
    return render_template('chapters.html', option=option, user=user)


@app.route('/chaptersCreate', methods=['POST'])
def chaptersCreate():
    try:
        user = session['USER']
    except Exception as error:
        return redirect(url_for('login'))
    name = request.form['name']
    author = request.form['author_name']
    cover = request.form['cover']
    description = request.form['description']

    chapters = Mangas(name, description, author, cover)

    flash("Chapters Successfully Added")
    # return render_template('mangas.html', option='Create', error=True)
    return render_template('chapters.html', option='Create', sucess=True, user=user)


@app.route('/chaptersUpdate', methods=['POST'])
def chaptersUpdate():
    try:
        user = session['USER']
    except Exception as error:
        return redirect(url_for('login'))
    name = request.form['name']
    author = request.form['author_name']
    cover = request.form['cover']
    description = request.form['description']

    chapters = Mangas(name, description, author, cover)

    flash("Chapters Updated Successfully")
    # return render_template('mangas.html', option='Create', error=True)
    return render_template('chapters.html', option='Update', sucess=True, user=user)


@app.route('/chaptersDelete', methods=['POST'])
def chaptersDelete():
    try:
        user = session['USER']
    except Exception as error:
        return redirect(url_for('login'))
    name = request.form['name']
    author = request.form['author_name']
    cover = request.form['cover']
    description = request.form['description']

    chapters = Mangas(name, description, author, cover)

    flash("Manga Successfully Deleted")
    # return render_template('mangas.html', option='Create', error=True)
    return render_template('chapters.html', option='Delete', sucess=True, user=user)


@app.route('/addUser', methods=['GET', 'POST'])
def addUser():
    if request.method == 'GET':
        try:
            user = session['USER']
            return render_template('addUser.html', user=user)
        except Exception as error:
            return redirect(url_for('login'))
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        adm = AdministratorDao(db)
        email = request.form['email']
        password = request.form['password']
        password_hash = hashlib.sha256(
            str(password).encode('utf-8')).hexdigest()
        user = Administrator(None, email, None)
        adm_user = adm.getAdmin(email)
        if adm_user != None and adm_user.password == password_hash:
            session['USER'] = adm_user.id
            flash("Successfully Logged In")
            return redirect(url_for('home'))
        else:
            flash("Incorrect Email/Username or Password")
            return render_template('login.html', user=user)


@app.route('/signout')
def signout():
    session['USER'] = None
    flash("User Logged Out Successfully")
    return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('500.html'), 404
