#<==================================================================================================>
#                                      IMPORTS
#<==================================================================================================>
import sys
import os
import csv
import uuid
import shutil
import pandas as pd
sys.path.append("../")
from pymongo import MongoClient
from common_utilities import CONSTANT


#<==================================================================================================>
#                                  FILE PROCESSING
#<==================================================================================================>
def inv_file_process(file_obj, is_inv):
    file_name = file_obj.filename.replace(' ', '').split('.', 1)[0]

    file_location = f"{os.getcwd()}/{str(uuid.uuid4())}"
    if os._exists(file_location):
        shutil.rmtree(file_location)

    os.mkdir(file_location)
    with open(f"{file_location}/{file_name}", 'wb') as f:
        f.write(file_obj.read())

    try:
        read_file = pd.read_excel(f'{file_location}/{file_name}')
        file_path = f'{file_location}/{file_name}.csv'
        read_file.to_csv(file_path)
    except:
        return False

    remote_mongo_uri = CONSTANT.TEST_DB_CLUSTER.value
    mongo_client = MongoClient(remote_mongo_uri)
    db = mongo_client.admin

    if is_inv:
        keys = inv_keys()
        return investor_file_processing(file_path, keys, db.investor, file_location)
    else:
        keys = str_keys()
        return startup_file_processing(file_path, keys, db.startup, file_location)


def investor_file_processing(file_path, keys, collection, file_location):
    input = csv.DictReader(open(file_path))
    for i in input:
        obj = {}
        for k, v in i.items():
            if k in keys:
                k = keys[k]
                if k in ("sectors", "syndicate"):
                    if v:
                        obj[k] = v.split(',')
                    else:
                        obj[k] = []
                else:
                    obj[k] = v.strip()
        try:
            collection.insert_one(obj)
        except:
            continue
    shutil.rmtree(file_location)
    return True


def startup_file_processing(file_path, keys, collection, file_location):
    input = csv.DictReader(open(file_path))
    for i in input:
        obj = {}
        for k, v in i.items():
            if k in keys:
                k = keys[k]
                if k in ("sectors", "progress"):
                    if v:
                        obj[k] = v.split(',')
                    else:
                        obj[k] = []
                else:
                    obj[k] = v.strip()
        try:
            collection.insert_one(obj)
        except:
            continue
    shutil.rmtree(file_location)
    return True


def str_keys():
    str_key = {
        "Email": "email",
        "Short Bio": "bio",
        "URL": "company_link",
        "Last Name": "last_name",
        "First Name": "first_name",
        "Your Position": "position",
        "Your Full Name": "full_name",
        "Startup Name?": "company_name",
        "1-2 Sentence Pitch": "startup_pitch",
        "What sector is your startup in?": "sectors",
        "What is your total round size?": "round_size",
        "How much have you already raised?": "raised",
        "Where is your startup's HQ located?": "location",
        "Select your three most impressive milestones": "progress",
    }
    return str_key


def inv_keys():
    inv_key = {
        "Email": "email",
        "Last Name": "last_name",
        "First Name": "first_name",
        "Where are you located?": "location",
        "Are you accredited?": "accreditation",
        "What sectors are you interested in?": "sectors",
        "Are you part of an Angel Group or Syndicate?": "angel",
        "How would you describe yourself in 1-2 sentances": "bio",
        "How much are you looking to invest in a given deal?": "deals"
    }
    return inv_key
