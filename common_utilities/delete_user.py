#<==================================================================================================>
#                                      IMPORTS
#<==================================================================================================>
import sys
sys.path.append('../')
from common_utilities import CONSTANT
from project.models import Investor, Startup


#<==================================================================================================>
#                                   DELETE A USER
#<==================================================================================================>
def delete_a_user(email, is_inv):
    collection = Investor if is_inv else Startup
    user_obj = collection.objects.filter(email=email).first()
    if user_obj:
        user_obj.delete()
        delete_user_from_ml(email, is_inv)
        return {"result": True, "error": "user delete successfully"}
    else:
        return {"result": False, "error": "user does not exist"}


#<==================================================================================================>
#                                   DELETE A USER
#<==================================================================================================>
def delete_user_from_ml(email, is_inv):
    from pymongo import MongoClient
    remote_mongo_uri = CONSTANT.CURRENT_DATABASE.value
    mongo_client = MongoClient(remote_mongo_uri)
    db = mongo_client["matching"]
    collection = db["users"]

    user_query = {"email": email, "investor": is_inv}
    collection.delete_one(user_query)
    return
