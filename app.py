from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import os
from db import db

app = Flask(__name__) 
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
# db = SQLAlchemy(app)

from views import * #só importar depois da config do app.

if __name__ == '__main__':
    app.run(debug=os.environ.get("DEBUG"))