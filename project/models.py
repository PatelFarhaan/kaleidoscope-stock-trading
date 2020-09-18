#<==================================================================================================>
#                                      IMPORTS
#<==================================================================================================>
import datetime
from flask_login import UserMixin
from project import db, login_manager


#<==================================================================================================>
#                                 USER LOADER LOGIN CLASS
#<==================================================================================================>
@login_manager.user_loader
def user_load(user_id):
    return User.objects.get(pk=user_id)
#
#
# #<==================================================================================================>
# #                                     ADMIN COLLECTION
# #<==================================================================================================>
# class User(db.Document, UserMixin):
#     password = db.StringField()
#     email = db.EmailField(required=True, unique=True)
#     created = db.DateTimeField(default=datetime.datetime.now)
#
#     def get_id(self):
#         return str(self.id)
#
#     meta = dict(indexes=['email'])



#<==================================================================================================>
#                                    INVESTOR COLLECTION
#<==================================================================================================>
class Shares(db.Document):
    share_name = db.StringField(unique=True)
    available_number = db.IntField(default=0)

    meta = dict(indexes=['share_name'])


#<==================================================================================================>
#                                    INVESTOR COLLECTION
#<==================================================================================================>
class Transaction(db.Document):
    date = db.StringField()
    email = db.EmailField()
    side = db.StringField()
    ticker = db.StringField()
    trader = db.StringField()
    share_number = db.IntField(default=0)

    meta = dict(indexes=['trader'])


#<==================================================================================================>
#                                    INVESTOR COLLECTION
#<==================================================================================================>
class User(db.Document, UserMixin):
    password = db.StringField()
    share_holding = db.DictField()
    email = db.EmailField(required=True, unique=True)
    created = db.DateTimeField(default=datetime.datetime.now)

    def get_id(self):
        return str(self.id)

    meta = dict(indexes=['email'])