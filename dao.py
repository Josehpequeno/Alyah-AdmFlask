from models import Mangas
import json
# import pprint


class MangasDao:
    def __init__(self, db):
        self.__db = db

    def getAllMangas(self):
        cursor = self.__db.cursor()
        cursor.execute("SELECT * FROM mangas")
        # records = cursor.fetchall()
        # row_count = 0
        results = []
        for row in cursor:
            # row_count += 1
            # print ("row: %s    %s\n" % (row_count, row))
            id = row[0]
            name= row[1]
            description = row[2]
            author = row[3]
            cover = row[4]
            manga = Mangas(name,description,author,cover,id)
            # j = {
            #     "name": name, 
            #     "description": description, 
            #     "author": author, 
            #     "cover": cover 
            # }
            # y = json.dumps(j)
            results.append(manga)
        # pprint.pprint(records)

        return results
