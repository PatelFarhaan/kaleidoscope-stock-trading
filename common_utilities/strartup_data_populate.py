#<==================================================================================================>
#                                       IMPORTS
#<==================================================================================================>
import sys
import csv
import ast
import shutil
sys.path.append("../")
from pymongo import MongoClient
from project.models import Startup
from common_utilities import CONSTANT
from project.serialise_class import StartupMLSchema


#<==================================================================================================>
#                                      STARTUP DATA DUMP
#<==================================================================================================>
def startup_data(csv_path, file_location):
    collection = db_connection_details()
    progress = progress_mapping()
    sectors_det = sectors_data()
    ma_schema = StartupMLSchema()

    input = csv.DictReader(open(csv_path))
    for i in input:
        i = dict(i)
        del i['']
        i["progress"] = [ progress[ele.strip()] for ele in i["progress"].split(',') ]
        i["sectors"] = [ sectors_det[j.strip()] for j in i["sectors"].split(',') if j != ""]

        if i["co_founders"] == "":
            i["co_founders"] = []
        else:
            i["co_founders"] = list(ast.literal_eval(i["co_founders"]))

        if i["num_team_members"] == "":
            i["num_team_members"] = 0
        else:
            i["num_team_members"] = int(float(i["num_team_members"]))

        round_size = round_def(int(i["round_size"]))
        i["round_size"] = int(i["round_size"])
        i["raised"] = int(float(i["raised"]))
        i["email_confirmed"] = False
        i["approved"] = False


        email = i["email"]
        users_count = collection.estimated_document_count()
        if users_count == 0:
            _id = 0
        else:
            _id = (((users_count - 1) * 100) + 100)

        i = {k:(v if v != "" else None) for k,v in i.items()}

        str_obj = Startup(**i)
        str_obj.save()

        str_obj = Startup.objects.filter(email=email).first()
        resp = ma_schema.dump(str_obj)
        resp["_id"] = _id
        resp["deals"] = [round_size]
        collection.insert_one(resp)

    shutil.rmtree(file_location)
    return True


#<==================================================================================================>
#                                   DATABASE CONNECTION DETAILS
#<==================================================================================================>
def db_connection_details():
    remote_mongo_uri = CONSTANT.TEST_DB_CLUSTER.value
    mongo_client = MongoClient(remote_mongo_uri)
    db = mongo_client.matching
    collection = db.users
    return collection


#<==================================================================================================>
#                                  PROGRESS MAPPING :=> STARTUP
#<==================================================================================================>
def progress_mapping():
    return {
        "Ideas/Sketches": "ideas",
        "Mockups/Renderings": "mockups",
        "Prototype/Pre-Launch": "prototype",
        "Beta Launched": "beta",
        "Taking Preorders": "preorders",
        "Product Launched": "product",
        "Early Users Acquired": "users",
        "Early Revenue Generated": "revenue"
    }


#<==================================================================================================>
#                                  ROUNDING FUNCTION :=> STARTUP
#<==================================================================================================>
def round_def(number):
    if 0 <= number <= 10000:
        return "0"
    elif 10000 <= number <= 25000:
        return "10"
    elif 25000 <= number <= 50000:
        return "25"
    elif 50000 <= number <= 100000:
        return "50"
    elif 100000 <= number <= 250000:
        return "100"
    elif 250000 <= number <= 500000:
        return "250"
    elif number > 500000:
        return "500"


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