# -*- coding: utf-8 -*-

from main import db

class Users(db.Document):
    username = db.StringField(required=True)
    password = db.StringField(required=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)

    @classmethod
    def check_user_passwd(cls, username, password):
        is_valid = None

        try:
            Users.objects.get(username=username, password=password)
        except Users.DoesNotExist:
            is_valid = False
        else:
            is_valid = True

        return is_valid
