import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
# DEBUG = True
# ENV = 'development'
# Connect to the database
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://alamjads_admin:3fWg8qzKlF[K@localhost:3306/alamjads_api?charset=utf8'

JSON_AS_ASCII = False
