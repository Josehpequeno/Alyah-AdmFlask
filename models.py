import hashlib
import re


def isEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True

    else:
        return False


class Author:
    def __init__(self, name, id=None):
        self.name = name
        self.id = id


class Administrator:
    def __init__(self, name, email, password, password_hash=None, id=None):
        self.name = name
        self.email = email
        if password_hash == None:
            password_hash = hashlib.sha256(
                str(password).encode('utf-8')).hexdigest()
        self.password = password_hash
        self.id = id

    def checkAdm(self, name, email, password):
        if len(name) < 3:
            return 'Name must be at least 3 characters'
        elif not isEmail(email):
            return 'Incorrectly filled in Email field'
        elif len(password) == 0:
            return 'Administrator password is empty'
        else:
            return True


class Mangas:
    def __init__(self, name, description, author, cover, id=None):
        self.name = name
        self.description = description
        self.author = author
        self.cover = cover
        self.id = id
        str = f'"id": "{id}", "name": "{name}","description": "{description}","author": "{author}","cover": "{cover}"'
        self.str = "{"+str+"}"


class Chapter:
    def __init__(self, name, manga, id=None):
        self.name = name
        self.manga = manga
        self.id = id
        str = f'"id": "{id}", "name": "{name}", "manga": "{manga}"'
        self.str = "{"+str+"}"


class Images:
    def __init__(self, url, chapter_id, id=None):
        self.url = url
        self.chapter_id = chapter_id
        self.id = id
        str = f'"id": "{id}", "url": "{url}", "chapter_id": "{chapter_id}"'
        self.str = "{"+str+"}"
