#<==================================================================================================>
#                                         IMPORTS
#<==================================================================================================>
import sys
import json
import requests
sys.path.append("../")
from pymongo import MongoClient
from common_utilities import CONSTANT


#<==================================================================================================>
#                                   DATABASE DETAILS
#<==================================================================================================>
def db_details(**kwargs):
    remote_mongo_uri = CONSTANT.CURRENT_DATABASE.value
    mongo_client = MongoClient(remote_mongo_uri)
    db = mongo_client.matching
    if kwargs.get("collection"):
        collection_name = kwargs.get("collection")
        collection = db[collection_name]
    else:
        collection = db.users
    return collection


#<==================================================================================================>
#                                 UPDATE INTO MATCHING
#<==================================================================================================>
def update_into_matching(email: str, new_count: int, is_inv: bool) -> bool:
    collection = db_details()
    my_query = {"email": email, "investor": is_inv}
    newvalues = { "$set": {"show_limit": new_count, "matched_week": 0} }

    try:
        collection.update_one(my_query, newvalues)
    except:
        return False
    return True


#<==================================================================================================>
#                                       CLEAN DISCOVER
#<==================================================================================================>
def clean_discover():
    url = "***REMOVED_SERVER_URL***/ml/api/v1/clean_discover"
    payload = {}
    headers = {
        'x-auth-key': "\')*9s`\\+Ex*M,$<W"
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    return response.json()