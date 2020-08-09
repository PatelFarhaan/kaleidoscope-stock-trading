#<==================================================================================================>
#                                       IMPORTS
#<==================================================================================================>
import sys
sys.path.append("../")
from pymongo import MongoClient
from flask import redirect, url_for
from common_utilities import CONSTANT
from project.models import Investor, Startup


#<==================================================================================================>
#                                  ACCOUNT DIS-APPROVE: INV + STR
#<==================================================================================================>
def disapprove_account(user_email, is_inv):
    collection = Investor if is_inv else Startup
    redirect_url = 'admin.investor_account' if is_inv else 'admin.startup_account'

    user_obj = collection.objects.filter(email=user_email).first()
    if not user_obj:
        return redirect(url_for(redirect_url))

    user_obj.approved = False
    user_obj.save()
    user_collection_update(user_email, is_inv)


#<==================================================================================================>
#                                   USER COLLECTION UPDATE
#<==================================================================================================>
def user_collection_update(email, is_inv):
    remote_mongo_uri = CONSTANT.CURRENT_DATABASE.value
    mongo_client = MongoClient(remote_mongo_uri)
    db = mongo_client.matching
    collection = db.users

    my_query = {"email": email, "investor": is_inv}
    newvalues = {"$set": {"approved": False}}

    try:
        collection.update_one(my_query, newvalues)
    except:
        pass

    return