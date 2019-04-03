import sqlite3
import os


class DBConnection:
    __PATH_TO_DB = "database/data.db"
    if not os.path.exists(__PATH_TO_DB):
        os.mkdir("database")

    __con = sqlite3.connect(__PATH_TO_DB)
    cursor = __con.cursor()

    @staticmethod
    def add_member(member):
        member_data_tuple = (
            member.first_name,
            member.last_name,
            member.hasDuplicateFirstName,
            member.canBeStage,
            member.canRotateMic,
            member.canAssist2ndHall,
            member.sundayException
        )

        query = "INSERT INTO member_info " \
                "(firstName," \
                "lastName," \
                "hasDuplicateFirstName," \
                "canBeStage," \
                "canRotateMic," \
                "canAssist2ndHall," \
                "sundayException) VALUES " \
                "(?, ?, ?, ?, ?, ?, ?)"
        DBConnection.cursor.execute(query, member_data_tuple)

    @staticmethod
    def remove_member(member):
        query = "DELETE FROM member_info WHERE member_info.id = ?"
        DBConnection.cursor.execute(query, member.ID)

    @staticmethod
    def update_member(member):
        member_data_tuple = (
            member.first_name,
            member.last_name,
            member.hasDuplicateFirstName,
            member.canBeStage,
            member.canRotateMic,
            member.canAssist2ndHall,
            member.sundayException,
            member.ID
        )

        query = "UPDATE member_info SET" \
                "firstName = ?," \
                "lastName = ?," \
                "hasDuplicateFirstName = ?" \
                "canBeStage = ?," \
                "canRotateMic = ?," \
                "canAssist2ndHall = ?," \
                "sundayException = ? WHERE member_info.id = ?"
        DBConnection.cursor.execute(query, member_data_tuple)
