from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from app import app, db
from dao import MangasDao, AdministratorDao, AuthorDao
from models import Administrator, Mangas, Chapter
import hashlib


def getUserSession():
    try:
        return session['USER']
    except Exception as error:
        return None


@app.route('/')  # definição de uma rota
def home():
    mangas_dao = MangasDao(db)
    mangas = mangas_dao.getAllMangas()
    user = getUserSession()
    return render_template('home.html', mangas=mangas, user=user)
    # tem que estar na pasta de templates


@app.route('/authors/<string:option>', methods=['GET', 'POST'])
def authors(option):
    user = getUserSession()
    if request.method == 'GET':
        if user == None:
            return redirect(url_for('login'))
        author_dao = AuthorDao(db)
        authors = author_dao.getAllAuthors()
        return render_template('authors.html', option=option, user=user, authors=authors)
    else:
        id = request.form['name']
        author_dao = AuthorDao(db)
        if id == "-1":
            flash('Choose A Valid Option')
            authors = author_dao.getAllAuthors()
            return render_template('authors.html', option=option, user=user, authors=authors, error=True)
        author_dao.delete(id)
        authors = author_dao.getAllAuthors()
        return render_template('authors.html', option=option, user=user, authors=authors, sucess=True)


@app.route('/mangas/<string:option>')
def mangas(option):
    user = getUserSession()
    if user == None:
        return redirect(url_for('login'))
    mangas_dao = MangasDao(db)
    mangas = mangas_dao.getAllMangas()
    return render_template('mangas.html', option=option, user=user, mangas=mangas)


@app.route('/mangasCreate', methods=['POST'])
def mangasCreate():
    user = getUserSession()
    if user == None:
        return redirect(url_for('login'))
    name = request.form['name']
    author = request.form['author_name']
    cover = request.form['cover']
    description = request.form['description']

    manga = Mangas(name, description, author, cover)
    mangasDao = MangasDao(db)
    create = mangasDao.create(manga)
    mangas = mangasDao.getAllMangas()
    if create == True:
        flash("Manga Successfully Added")
        return render_template('mangas.html', option='Create', sucess=True, user=user, mangas=mangas)
    elif create == False:
        flash("Manga Name Already In Use")
        return render_template('mangas.html', option='Create', error=True, user=user, mangas=mangas)
    else:
        flash("Failed To Add Manga")
        return render_template('mangas.html', option='Create', error=True, user=user, mangas=mangas)


@app.route('/mangasUpdate', methods=['POST'])
def mangasUpdate():
    user = getUserSession()
    if user == None:
        return redirect(url_for('login'))
    name = request.form['current_name']
    new_name = request.form['new_name']
    author = request.form['author_name']
    cover = request.form['cover']
    description = request.form['description']
    id = request.form['id']

    manga = Mangas(new_name, description, author, cover, id)
    mangasDao = MangasDao(db)
    mangas = mangasDao.getAllMangas()
    if name != new_name:
        check = mangasDao.checkName(new_name)
        if check == False:
            flash("Manga Name Already In Use")
            return render_template('mangas.html', option='Update', error=True, user=user, mangas=mangas)

    update = mangasDao.update(manga)
    mangas = mangasDao.getAllMangas()
    if update == True:
        flash("Manga Updated Successfully")
        return render_template('mangas.html', option='Update', sucess=True, user=user, mangas=mangas)
    else:
        print(update)
        flash("Failed To Update Manga")
        return render_template('mangas.html', option='Update', error=True, user=user, mangas=mangas)


@app.route('/mangasDelete', methods=['POST'])
def mangasDelete():
    user = getUserSession()
    if user == None:
        return redirect(url_for('login'))
    id = request.form['name']
    # manga = Mangas(name, description, author, cover)
    mangasDao = MangasDao(db)
    mangas = mangasDao.getAllMangas()
    if id == "-1":
        flash('Choose A Valid Option')
        return render_template('mangas.html', option='Delete', error=True, user=user, mangas=mangas)
    mangasDao.delete(id)
    flash("Manga Successfully Deleted")
    mangas = mangasDao.getAllMangas()
    return render_template('mangas.html', option='Delete', sucess=True, user=user, mangas=mangas)


@app.route('/chapters/<string:option>')
def chapters(option):
    user = getUserSession()
    if user == None:
        return redirect(url_for('login'))
    return render_template('chapters.html', option=option, user=user)


@app.route('/chaptersCreate', methods=['POST'])
def chaptersCreate():
    user = getUserSession()
    if user == None:
        return redirect(url_for('login'))
    name = request.form['name']
    manga = request.form['manga']
    urls = request.form['urls']

    chapters = Chapter(name, manga)

    flash("Chapters Successfully Added")
    # return render_template('mangas.html', option='Create', error=True)
    return render_template('chapters.html', option='Create', sucess=True, user=user)


@app.route('/chaptersUpdate', methods=['POST'])
def chaptersUpdate():
    user = getUserSession()
    if user == None:
        return redirect(url_for('login'))
    name = request.form['name']
    new_name = request.form['new_name']
    manga = request.form['manga']
    urls = request.form['urls']

    chapters = Chapter(name, manga)

    flash("Chapters Updated Successfully")
    # return render_template('mangas.html', option='Create', error=True)
    return render_template('chapters.html', option='Update', sucess=True, user=user)


@app.route('/chaptersDelete', methods=['POST'])
def chaptersDelete():
    user = getUserSession()
    if user == None:
        return redirect(url_for('login'))
    name = request.form['name']

    flash("Manga Successfully Deleted")
    # return render_template('mangas.html', option='Create', error=True)
    return render_template('chapters.html', option='Delete', sucess=True, user=user)


@app.route('/addUser', methods=['GET', 'POST'])
def addUser():
    user = getUserSession()
    if request.method == 'GET':
        if user == None:
            return redirect(url_for('login'))
        else:
            return render_template('addUser.html', user=user)
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        adm = Administrator(name, email, password)
        check = Administrator.checkAdm(adm, name, email, password)
        if check != True:
            flash(check)
            return render_template('addUser.html', user=user, adm=adm, error=True)
        if confirm_password != password:
            flash('Passwords do not match')
            return render_template('addUser.html', user=user, adm=adm, error=True)
        administratorDao = AdministratorDao(db)
        if administratorDao.checkEmail(adm.email):
            if administratorDao.checkName(adm.name):
                result = administratorDao.add(adm)
                if result:
                    flash('Administrator Added Successfully')
                    return render_template('addUser.html', user=user, adm=adm, sucess=True)
                else:
                    print("Error: " + result)
                    flash('Administrator Not Added')
                    return render_template('addUser.html', user=user, adm=adm, error=True)
            else:
                flash('Name Already In Use')
                return render_template('addUser.html', user=user, adm=adm, error=True)
        else:
            flash('Email Already In Use')
            return render_template('addUser.html', user=user, adm=adm, error=True)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    userId = getUserSession()
    if request.method == 'GET':
        if userId == None:
            return redirect(url_for('login'))
        else:
            adm = AdministratorDao(db)
            adm_user = adm.getAdminById(userId)
            return render_template('profile.html', user=userId, adm=adm_user)
    else:
        admDao = AdministratorDao(db)
        adm_user = admDao.getAdminById(userId)
        name = request.form['name']
        email = request.form['email']
        current_password = request.form['current_password']
        password_hash = hashlib.sha256(
            str(current_password).encode('utf-8')).hexdigest()
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        adm = Administrator(name, email, current_password)
        if adm_user != None and adm_user.password == password_hash:
            check = Administrator.checkAdm(adm, name, email, current_password)
            if check != True:
                flash(check)
                return render_template('profile.html', user=userId, adm=adm, error=True)
            if confirm_password != password:
                flash('Passwords do not match')
                return render_template('profile.html', user=userId, adm=adm, error=True)
            if password != "":
                adm = Administrator(name, email, password)
            administratorDao = AdministratorDao(db)
            if email == adm_user.email or administratorDao.checkEmail(adm.email):
                if name == adm_user.name or administratorDao.checkName(adm.name):
                    result = administratorDao.update(adm, userId)
                    if result:
                        flash('Administrator Updated Successfully')
                        return render_template('profile.html', user=userId, adm=adm, sucess=True)
                    else:
                        print("Error: " + result)
                        flash('Administrator Not Updated')
                        return render_template('profile.html', user=userId, adm=adm, error=True)
                else:
                    flash('Name Already In Use')
                    return render_template('profile.html', user=userId, adm=adm, error=True)
            else:
                flash('Email Already In Use')
                return render_template('profile.html', user=userId, adm=adm, error=True)
        else:
            flash("Incorrect Password")
            return render_template('profile.html', user=userId, adm=adm, error=True)


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
