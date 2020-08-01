#<==================================================================================================>
#                                       IMPORTS
#<==================================================================================================>
import sys
import csv
import shutil
import random
import string
sys.path.append("../")
from pymongo import MongoClient
from common_utilities import CONSTANT
from itsdangerous import URLSafeTimedSerializer
from project.serialise_class import InvestorMLSchema
from werkzeug.security import generate_password_hash
from project.models import Investor, InvestorBetaData


#<==================================================================================================>
#                                      INVESTOR DATA DUMP
#<==================================================================================================>
def investor_beta_data(csv_path, file_location):
    ma_schema = InvestorMLSchema()
    collection = db_connection_details()

    input = csv.DictReader(open(csv_path))
    for i in input:
        i = dict(i)
        del i['']
        i["approved"] =  False
        email = i["email"].lower()
        i["email_confirmed"] = False
        password = get_random_password()
        i["password"] = generate_password_hash(password)
        confirmation_link = confirmation_link_generator(email)
        i["passowrd_confirm_meta_data"] = {"is_clicked": False}

        inv_beta_obj = InvestorBetaData(email=email,
                                        password=password,
                                        confirmation_link=confirmation_link)
        inv_beta_obj.save()

        users_count = collection.estimated_document_count()
        if users_count == 0:
            _id = 0
        else:
            _id = list(collection.find().skip(users_count-1))[0].get("_id") + 100

        try:
            new_obj = Investor(**i)
            new_obj.save()

            inv_obj = Investor.objects.filter(email=email).first()
            resp = ma_schema.dump(inv_obj)
            resp["_id"] = _id
            collection.insert_one(resp)
        except:
            return False

    shutil.rmtree(file_location)
    return True


#<==================================================================================================>
#                                   DATABASE CONNECTION DETAILS
#<==================================================================================================>
def db_connection_details():
    remote_mongo_uri = CONSTANT.CURRENT_DATABASE.value
    mongo_client = MongoClient(remote_mongo_uri)
    db = mongo_client.matching
    collection = db.users
    return collection


#<==================================================================================================>
#                                   RANDOM PASSWORD GENERATOR
#<==================================================================================================>
def get_random_password(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


#<==================================================================================================>
#                                   CONFIRMATION LINK GENERATOR
#<==================================================================================================>
def confirmation_link_generator(email):
    serial = URLSafeTimedSerializer("***REMOVED_SECRET_KEY***")
    token = serial.dumps(email, salt='email_confirm')
    return f"{CONSTANT.CURRENT_SERVER.value}/api/v1/investor/email-confirmed/{token}"