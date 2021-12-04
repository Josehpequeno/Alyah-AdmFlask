from models import Mangas, Author
import json

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
            name= row[1]
            description = row[2]
            author_id = row[3]
            authorDao = AuthorDao(self.__db)
            author = authorDao.getAuthorName(author_id)
            cover = row[4]
            # favorites_count = row[5]
            manga = Mangas(name,description,author,cover,id)
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
    def getAuthorName(self,id):
        cursor = self.__db.cursor()
        cursor.execute(f"SELECT name FROM authors WHERE id = {id}")
        # print (cursor.fetchone()[0])
        return cursor.fetchone()[0]
