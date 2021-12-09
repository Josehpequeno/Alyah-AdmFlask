from models import Mangas, Author, Administrator


class MangasDao:
    def __init__(self, db):
        self.__db = db

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


class AuthorDao:
    def __init__(self, db):
        self.__db = db

    def getAuthorName(self, id):
        cursor = self.__db.cursor()
        cursor.execute(f"SELECT name FROM authors WHERE id = {id}")
        return cursor.fetchone()[0]


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
            cursor.execute("SELECT * FROM admin_user")
            records = cursor.fetchall()
            print("Select data is: ")
            for record in records:
                print(record)
            print()
            self.__db.commit()
            return True
        except Exception as error:
            return error
    def update(self, adm):
        pass
        # try:
        #     cursor = self.__db.cursor()
        #     cursor.execute("INSERT INTO admin_user (name, email, password) VALUES (%s,%s,%s)", [
        #         adm.name, adm.email, adm.password])
        #     self.__db.commit()
        #     cursor.execute("SELECT * FROM admin_user")
        #     records = cursor.fetchall()
        #     print("Select data is: ")
        #     for record in records:
        #         print(record)
        #     print()
        #     self.__db.commit()
        #     return True
        # except Exception as error:
        #     return error