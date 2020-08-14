#<==================================================================================================>
#                                       IMPORTS
#<==================================================================================================>
import sys
import csv
import ast
import json
import shutil
sys.path.append("../")
from pymongo import MongoClient
from project.models import Investor
from common_utilities import CONSTANT
from project.serialise_class import InvestorMLSchema
from werkzeug.security import generate_password_hash


#<==================================================================================================>
#                                      INVESTOR DATA DUMP
#<==================================================================================================>
def investor_data(csv_path, file_location):
    ma_schema = InvestorMLSchema()
    sectors_det = sectors_data()

    collection = db_connection_details()

    input = csv.DictReader(open(csv_path))
    for i in input:
        i = dict(i)

        email = i["email"].lower()
        user_exist_check = Investor.objects.filter(email=email).first()
        if user_exist_check:
            continue

        del i['']
        i["approved"] = False
        i["deals"] = [i["deals"]]
        i["email_confirmed"] = True
        i["password"] = generate_password_hash("Angelfund1!")
        i["sectors"] = [sectors_det[i.strip()] for i in i["sectors"].split(',')]
        i["syndicate"] = [i.strip() for i in i["syndicate"].split(',') if i.strip() != ""]

        try:
            i["prior_investments"] = [json.loads(json.dumps(i)) for i in ast.literal_eval(i["prior_investments"])]
        except:
            i["prior_investments"] = []

        try:
            i["accreditation"] = str(int(float(i["accreditation"])))
        except:
            i["accreditation"] = "nothing"

        users_count = collection.estimated_document_count()
        if users_count == 0:
            _id = 0
        else:
            _id = list(collection.find().skip(users_count-1))[0].get("_id") + 100

        new_obj = Investor(**i)
        new_obj.save()

        inv_obj = Investor.objects.filter(email=email).first()
        resp = ma_schema.dump(inv_obj)
        resp["_id"] = _id
        collection.insert_one(resp)

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
#                               SECTORS MAPPING :=> INVESTORS
#<==================================================================================================>
def sectors_data():
    return {'Agriculture / Agtech': 'agtech',
            'Artificial Intelligence': 'ai',
            'Augmented Reality': 'ar',
            'Biomedical': 'biomed',
            'Biotech': 'biotech',
            'Blockchain': 'blockchain',
            'Community': 'community',
            'Crowdfunding': 'crowdfund',
            'Developer Tools': 'devtools',
            'Diversity': 'diversity',
            'Drones': 'drones',
            'Education': 'education',
            'Energy': 'energy',
            'Enterprise': 'enterprise',
            'Entertainment': 'entertain',
            'Esports / Online Gaming': 'gaming',
            'Financial / Banking': 'banking',
            'Government': 'government',
            'Hardware': 'hardware',
            'Healthcare': 'health',
            'Marketplace': 'market',
            'Media / Advertising': 'media',
            'Moonshots / Hard Tech': 'hardtech',
            'Robotics': 'robotics',
            'Security': 'security',
            'Sport / Fitness': 'sport',
            'Transportation': 'transport',
            'Travel': 'travel',
            'Virtual Reality': 'vr',
            'Other': 'other'}