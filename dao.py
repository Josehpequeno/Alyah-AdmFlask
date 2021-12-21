from models import Mangas, Author, Administrator, Chapter, Images


class MangasDao:
    def __init__(self, db):
        self.__db = db

    def checkName(self, name):
        cursor = self.__db.cursor()
        cursor.execute("SELECT * FROM mangas")
        for row in cursor:
            if name == row[1]:
                return False
        return True

    def getAllMangas(self):
        cursor = self.__db.cursor()
        cursor.execute("SELECT * FROM mangas")
        # records = cursor.fetchall()
        results = []
        for row in cursor:
            id = row[0]
            name = row[1]
            description = row[2]
            author_id = row[3]
            authorDao = AuthorDao(self.__db)
            author = authorDao.getAuthorName(author_id)
            cover = row[4]
            # favorites_count = row[5]
            manga = Mangas(name, description, author, cover, id)
            # j = {
            #     "name": name,
            #     "description": description,
            #     "author": author,
            #     "cover": cover
            # }
            # y = json.dumps(j)
            results.append(manga)
        return results

    def create(self, manga):
        try:
            authorDao = AuthorDao(self.__db)
            author_id = authorDao.getAuthorId(manga.author)
            # if author_id == False:
            #     raise Exception("ERROR in the database")
            # else:
            if author_id == None:
                authorDao.create_author(manga.author)
                author_id = authorDao.getAuthorId(manga.author)
            if self.checkName(manga.name) == False:
                return False
            cursor = self.__db.cursor()
            cursor.execute("INSERT INTO mangas (name, description, author_id, cover) VALUES (%s,%s,%s,%s)", [
                manga.name, manga.description, author_id, manga.cover])
            self.__db.commit()
            return True
        except Exception as error:
            return error

    def delete(self, id):
        try:
            cursor = self.__db.cursor()
            cursor.execute("DELETE FROM mangas WHERE id = %s", [id])
            self.__db.commit()
            return True
        except Exception as error:
            return error

    def update(self, manga):
        try:
            authorDao = AuthorDao(self.__db)
            author_id = authorDao.getAuthorId(manga.author)
            if author_id == None:
                authorDao.create_author(manga.author)
                author_id = authorDao.getAuthorId(manga.author)
            cursor = self.__db.cursor()
            cursor.execute("UPDATE mangas SET name = %s, description = %s, author_id = %s, cover = %s WHERE id = %s",
                           [manga.name, manga.description, author_id, manga.cover, manga.id])
            self.__db.commit()
            return True
        except Exception as error:
            return error


class AuthorDao:
    def __init__(self, db):
        self.__db = db

    def getAllAuthors(self):
        cursor = self.__db.cursor()
        cursor.execute("SELECT * FROM authors")
        # records = cursor.fetchall()
        results = []
        for row in cursor:
            id = row[0]
            name = row[1]
            # favorites_count = row[5]
            author = Author(name, id)
            # j = {
            #     "name": name,
            #     "description": description,
            #     "author": author,
            #     "cover": cover
            # }
            # y = json.dumps(j)
            results.append(author)
        return results

    def getAuthorName(self, id):
        try:
            cursor = self.__db.cursor()
            cursor.execute(f"SELECT name FROM authors WHERE id = {id}")
            return cursor.fetchone()[0]
        except Exception as error:
            cursor = self.__db.cursor()
            cursor.execute("ROLLBACK")
            self.__db.commit()
            return error

    def getAuthorId(self, name):
        try:
            cursor = self.__db.cursor()
            cursor.execute("SELECT id FROM authors WHERE name = %s", [name])
            results = cursor.fetchone()
            if type(results) != type(()):
                return None
            else:
                return results[0]
        except Exception as error:
            cursor = self.__db.cursor()
            cursor.execute("ROLLBACK")
            self.__db.commit()
            return error

    def create_author(self, name):
        try:
            cursor = self.__db.cursor()
            cursor.execute("INSERT INTO authors (name) VALUES (%s)", [name])
            self.__db.commit()
        except Exception as error:
            cursor = self.__db.cursor()
            cursor.execute("ROLLBACK")
            self.__db.commit()
            return error

    def delete(self, id):
        try:
            cursor = self.__db.cursor()
            cursor.execute("DELETE FROM authors WHERE id = %s", [id])
            self.__db.commit()
            return True
        except Exception as error:
            cursor = self.__db.cursor()
            cursor.execute("ROLLBACK")
            self.__db.commit()
            return error


class AdministratorDao:
    def __init__(self, db):
        self.__db = db

    def checkEmail(self, email):
        cursor = self.__db.cursor()
        cursor.execute("SELECT * FROM admin_user WHERE email = %s", [email])
        results = cursor.fetchall()
        if results != []:
            return False
        else:
            return True

    def checkName(self, name):
        cursor = self.__db.cursor()
        cursor.execute("SELECT * FROM admin_user WHERE name = %s", [name])
        results = cursor.fetchall()
        if results != []:
            return False
        else:
            return True

    def getAdmin(self, username):
        cursor = self.__db.cursor()
        cursor.execute("SELECT * FROM admin_user WHERE email = %s", [username])
        results = cursor.fetchall()
        if results != []:
            id = results[0][0]
            name = results[0][1]
            email = results[0][2]
            password = results[0][3]
            adm = Administrator(name, email, password, password, id)
            return adm
        else:
            cursor.execute(
                "SELECT * FROM admin_user WHERE name =  %s", [username])
            results = cursor.fetchall()
            if results != []:
                id = results[0][0]
                name = results[0][1]
                email = results[0][2]
                password = results[0][3]
                adm = Administrator(name, email, password)
                return adm
            else:
                return None

    def getAdminById(self, id):
        cursor = self.__db.cursor()
        cursor.execute("SELECT * FROM admin_user WHERE id = %s", [id])
        results = cursor.fetchall()
        if results != []:
            id = results[0][0]
            name = results[0][1]
            email = results[0][2]
            password = results[0][3]
            adm = Administrator(name, email, password, password, id)
            return adm
        else:
            return None

    def add(self, adm):
        try:
            cursor = self.__db.cursor()
            cursor.execute("INSERT INTO admin_user (name, email, password) VALUES (%s,%s,%s)", [
                adm.name, adm.email, adm.password])
            self.__db.commit()
            return True
        except Exception as error:
            cursor = self.__db.cursor()
            cursor.execute("ROLLBACK")
            self.__db.commit()
            return error

    def update(self, adm, id):
        try:
            cursor = self.__db.cursor()
            cursor.execute("UPDATE admin_user SET name = %s, email = %s, password = %s WHERE id = %s", [
                adm.name, adm.email, adm.password, id])
            self.__db.commit()
            return True
        except Exception as error:
            return error


class ChapterDao:
    def __init__(self, db):
        self.__db = db

    def checkName(self, name, manga_id):
        cursor = self.__db.cursor()
        cursor.execute(
            "SELECT * FROM chapters WHERE name = %s AND manga_id = %s", [name, manga_id])
        results = cursor.fetchall()
        if results != []:
            return False
        else:
            return True

    def create(self, name, manga_id):
        try:
            cursor = self.__db.cursor()
            cursor.execute("INSERT INTO chapters (name, manga_id) VALUES (%s,%s) RETURNING ID", [
                           name, manga_id])
            results = []
            id = 0
            for row in cursor:
                id = row[0]
            self.__db.commit()
            return (True, id)
        except Exception as error:
            cursor = self.__db.cursor()
            cursor.execute("ROLLBACK")
            self.__db.commit()
            return (False, error)

    def getAllChapters(self):
        cursor = self.__db.cursor()
        cursor.execute("SELECT * FROM chapters")
        results = []
        for row in cursor:
            id = row[0]
            name = row[1]
            manga = row[2]
            chapter = Chapter(name, manga, id)
            results.append(chapter)
        return results

    def getAllChaptersByMangaId(self, manga_id):
        cursor = self.__db.cursor()
        cursor.execute(
            "SELECT * FROM chapters WHERE manga_id = %s", [manga_id])
        results = []
        for row in cursor:
            id = row[0]
            name = row[1]
            manga = row[2]
            chapter = Chapter(name, manga, id)
            results.append(chapter.str)
        return results

    def delete(self, id):
        try:
            cursor = self.__db.cursor()
            cursor.execute("DELETE FROM chapters WHERE id = %s", [id])
            self.__db.commit()
            return True
        except Exception as error:
            cursor = self.__db.cursor()
            cursor.execute("ROLLBACK")
            self.__db.commit()
            return error

    def update(self, chapter):
        try:
            cursor = self.__db.cursor()
            cursor.execute("UPDATE chapters SET name = %s, manga_id = %s WHERE id = %s",
                           [chapter.name, chapter.manga, chapter.id])
            self.__db.commit()
            return True
        except Exception as error:
            cursor = self.__db.cursor()
            cursor.execute("ROLLBACK")
            self.__db.commit()
            return error


class ImagesDao:
    def __init__(self, db):
        self.__db = db

    def create(self, url, chapter_id):
        try:
            cursor = self.__db.cursor()
            cursor.execute("INSERT INTO images (url, chapter_id) VALUES (%s,%s)", [
                           url, chapter_id])
            self.__db.commit()
            return True
        except Exception as error:
            cursor = self.__db.cursor()
            cursor.execute("ROLLBACK")
            self.__db.commit()
            return error

    def getAllImagesByChapterId(self, chapter_id):
        cursor = self.__db.cursor()
        cursor.execute(
            "SELECT * FROM images WHERE chapter_id = %s", [chapter_id])
        results = []
        for row in cursor:
            id = row[0]
            url = row[1]
            # description = row[2] column a ser removida, sem uso.
            chapter_id = row[3]
            image = Images(url, chapter_id, id)
            results.append(image.url)
        return results

    def delete(self, chapter_id):
        try:
            cursor = self.__db.cursor()
            cursor.execute(
                "DELETE FROM images WHERE chapter_id = %s", [chapter_id])
            self.__db.commit()
            return True
        except Exception as error:
            cursor = self.__db.cursor()
            cursor.execute("ROLLBACK")
            self.__db.commit()
            return error
