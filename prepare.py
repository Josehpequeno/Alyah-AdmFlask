from db import db
import hashlib
import os
from dotenv import load_dotenv
load_dotenv()

cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS admin_user")
script = "CREATE TABLE IF NOT EXISTS admin_user (\
            ID SERIAL PRIMARY KEY,\
            name VARCHAR(40) NOT NULL UNIQUE,\
            email VARCHAR(50) NOT NULL,\
            password VARCHAR(255) NOT NULL)"
cursor.execute(script)
db.commit()
password = os.environ.get("SECRET")
password_hash = hashlib.sha256(
    str(password).encode('utf-8')).hexdigest()
cursor.execute("INSERT INTO admin_user (name, email, password) VALUES (%s,%s,%s)", [
               "Josehpequeno", "hicarojbs21@gmail.com", password_hash])
db.commit()

cursor.execute("SELECT * FROM admin_user")
records = cursor.fetchall()
print("Select data is: ")
for record in records:
    print(record)
print()
db.commit()
