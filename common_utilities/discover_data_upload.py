#<==================================================================================================>
#                                       IMPORTS
#<==================================================================================================>
import sys
import csv
import shutil
sys.path.append("../")
from project.models import Investor, Startup


#<==================================================================================================>
#                                 INVESTOR DISCOVER CARDS DATA DUMP
#<==================================================================================================>
def discover_cards_data(csv_path, file_location, is_inv):
    collection = Investor if is_inv else Startup

    input = csv.DictReader(open(csv_path))
    for i in input:
        i = dict(i)

        email = i["email"].lower()
        user_obj = collection.objects.filter(email=email).first()
        if not user_obj:
            continue

        try:
            _cards = [ i.strip() for i in i["discover_card_data"].split(',') ]
            existing_discover_cards = list(user_obj.discover_cards)
            existing_discover_cards.extend(_cards)
            user_obj.discover_cards = existing_discover_cards
            user_obj.save()
        except:
            return False

    shutil.rmtree(file_location)
    return True