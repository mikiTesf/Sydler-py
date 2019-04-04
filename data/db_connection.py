import sqlite3
import os
from data import member


class DBConnection:
    __PATH_TO_DB = "database/data.db"
    if not os.path.exists(__PATH_TO_DB):
        os.mkdir("database")

    __con = sqlite3.connect(__PATH_TO_DB)
    cursor = __con.cursor()

    @staticmethod
    def add_member(member):
        member_data = (
            member.first_name,
            member.last_name,
            member.has_sunday_exception,
            member.can_be_stage,
            member.can_rotate_mic,
            member.can_assist_2nd_hall,
            member.has_sunday_exception
        )

        query = "INSERT INTO member_info " \
                "(firstName," \
                "lastName," \
                "hasDuplicateFirstName," \
                "canBeStage," \
                "canRotateMic," \
                "canAssist2ndHall," \
                "sundayException) VALUES " \
                "(?, ?, ?, ?, ?, ?, ?);"
        DBConnection.cursor.execute(query, member_data)
        DBConnection.__con.commit()

    @staticmethod
    def remove_member(member_id):
        id_tuple = (member_id,)
        query = "DELETE FROM member_info WHERE member_info.id = ?;"
        DBConnection.cursor.execute(query, id_tuple)
        DBConnection.__con.commit()

    @staticmethod
    def update_member(member):
        member_data = (
            member.first_name,
            member.last_name,
            member.has_sunday_exception,
            member.can_be_stage,
            member.can_rotate_mic,
            member.can_assist_2nd_hall,
            member.has_sunday_exception,
            member.ID
        )

        query = "UPDATE member_info SET " \
                "firstName = ?," \
                "lastName = ?," \
                "hasDuplicateFirstName = ?," \
                "canBeStage = ?," \
                "canRotateMic = ?," \
                "canAssist2ndHall = ?," \
                "sundayException = ? WHERE member_info.id = ?;"
        DBConnection.cursor.execute(query, member_data)
        DBConnection.__con.commit()

    # getting a single or all members may be necessary sometimes
    @staticmethod
    def get_member(member_id):
        id_tuple = (member_id,)
        query = "SELECT * FROM member_info WHERE member_info.id = ?;"

        member_info = DBConnection.cursor.execute(query, id_tuple).fetchone()
        _member = member.Member()
        _member.ID = member_info[0]
        _member.first_name = member_info[1]
        _member.last_name = member_info[2]
        _member.first_name_is_duplicate = bool(member_info[3])
        _member.can_be_stage = bool(member_info[4])
        _member.can_rotate_mic = bool(member_info[5])
        _member.can_assist_2nd_hall = bool(member_info[6])
        _member.has_sunday_exception = bool(member_info[7])

        return _member

    @staticmethod
    def get_all_members():
        query = "SELECT * FROM member_info;"
        all_members = []

        for member_info in DBConnection.cursor.execute(query).fetchall():
            _member = member.Member()
            _member.ID = member_info[0]
            _member.first_name = member_info[1]
            _member.last_name = member_info[2]
            _member.first_name_is_duplicate = bool(member_info[3])
            _member.can_be_stage = bool(member_info[4])
            _member.can_rotate_mic = bool(member_info[5])
            _member.can_assist_2nd_hall = bool(member_info[6])
            _member.has_sunday_exception = bool(member_info[7])
            all_members.append(_member)

        return all_members
