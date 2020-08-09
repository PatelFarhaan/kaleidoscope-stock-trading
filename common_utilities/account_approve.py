#<==================================================================================================>
#                                       IMPORTS
#<==================================================================================================>
import sys
import threading
sys.path.append("../")
from pymongo import MongoClient
from flask import redirect, url_for
from common_utilities import CONSTANT
from project.models import Investor, Startup
from common_utilities.wait_list_completed_startup import wait_list_over_str
from common_utilities.wait_list_completed_investor import wait_list_over_inv


#<==================================================================================================>
#                                  ACCOUNT APPROVE: INV + STR
#<==================================================================================================>
def approve_account(user_email, is_inv):
    collection = Investor if is_inv else Startup
    email_target = wait_list_over_inv if is_inv else wait_list_over_str
    redirect_url = 'admin.investor_account' if is_inv else 'admin.startup_account'

    user_obj = collection.objects.filter(email=user_email).first()
    if not user_obj:
        return redirect(url_for(redirect_url))

    user_obj.approved = True
    user_obj.save()
    user_collection_update(user_email, is_inv)


    email, first_name = user_obj.email, user_obj.first_name
    thread = threading.Thread(target=email_target, args=(email, first_name,))
    thread.start()


#<==================================================================================================>
#                                   USER COLLECTION UPDATE
#<==================================================================================================>
def user_collection_update(email, is_inv):
    remote_mongo_uri = CONSTANT.CURRENT_DATABASE.value
    mongo_client = MongoClient(remote_mongo_uri)
    db = mongo_client.matching
    collection = db.users

    my_query = {"email": email, "investor": is_inv}
    newvalues = {"$set": {"approved": True}}

    try:
        collection.update_one(my_query, newvalues)
    except:
        pass

    return