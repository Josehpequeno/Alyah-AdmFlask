class Mangas:
    def __init__(self, name, description, author, cover, id=None):
        self.name = name
        self.description = description
        self.author = author
        self.cover = cover
        self.id = id

class Author: 
    def __init__(self, name, id=None):
        self.name = name
        self.id = id