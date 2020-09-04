#<==================================================================================================>
#                                       IMPORTS
#<==================================================================================================>
import sys
import csv
import shutil
import random
import string
sys.path.append("../")
from common_utilities import CONSTANT
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash
from project.models import Investor, InvestorBetaData


#<==================================================================================================>
#                                      INVESTOR DATA DUMP
#<==================================================================================================>
def investor_beta_data(csv_path, file_location):
    input = csv.DictReader(open(csv_path))
    for i in input:
        i = dict(i)

        email = i["email"].lower()
        user_exist_check = Investor.objects.filter(email=email).first()
        if user_exist_check:
            continue

        del i['']
        i["approved"] = False
        i["email_confirmed"] = False
        password = get_random_password()
        i["password"] = generate_password_hash(password)
        confirmation_link = confirmation_link_generator(email)
        i["passowrd_confirm_meta_data"] = {"is_clicked": False}

        inv_beta_obj = InvestorBetaData(email=email,
                                        password=password,
                                        confirmation_link=confirmation_link)
        inv_beta_obj.save()
        new_obj = Investor(**i)
        new_obj.save()

    shutil.rmtree(file_location)
    return True


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