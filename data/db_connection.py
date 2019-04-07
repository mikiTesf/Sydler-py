import sqlite3
from os import mkdir
from os import path


class DBConnection:
    __PATH_TO_DB = "../database/data.db"
    #########################################################################
    # checking for the existence of the database and connecting to it
    if not path.exists(__PATH_TO_DB):
        mkdir("../database")
    con = sqlite3.connect(__PATH_TO_DB)
    cursor = con.cursor()
    # checking for the existence of the table(s) inside the database
    table_creating_statement = 'CREATE TABLE IF NOT EXISTS member_info (' \
                               'id                    INTEGER ' \
                               'PRIMARY KEY AUTOINCREMENT,' \
                               'firstName             VARCHAR not null,' \
                               'lastName              VARCHAR not null,' \
                               'hasDuplicateFirstName BOOLEAN not null,' \
                               'canBeStage            BOOLEAN,' \
                               'canRotateMic          BOOLEAN,' \
                               'canAssist2ndHall      BOOLEAN,' \
                               'sundayException       BOOLEAN' \
                               ');'
    cursor.execute(table_creating_statement)
    #########################################################################
