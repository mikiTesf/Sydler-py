from peewee import Model, CharField, BooleanField
from sydler.data.db_connection import DB


class Member(Model):
    first_name = CharField()
    last_name = CharField()
    first_name_is_duplicate = BooleanField()
    can_be_stage = BooleanField()
    can_rotate_mic = BooleanField()
    can_assist_2nd_hall = BooleanField()
    has_sunday_exception = BooleanField()

    def __str__(self):
        self.first_name + ' ' + self.last_name

    class Meta:
        database = DB
        table_name = 'member_info'


# create the 'member_info' table in case it doesn't exist
DB.create_tables([Member])
