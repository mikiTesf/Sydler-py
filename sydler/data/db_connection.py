from os import path, environ, makedirs
from peewee import SqliteDatabase

CACHE_FOLDER_NAME = '.sydler'
DB_FILE_NAME = 'member.db'
# create the cache folder before connecting to the data store
path_to_db = path.join(environ.get('HOME'), CACHE_FOLDER_NAME)
makedirs(path_to_db, exist_ok=True)
# create and connect to data store
DB = SqliteDatabase(path.join(path_to_db, DB_FILE_NAME))
DB.connect()
