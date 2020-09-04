#<==================================================================================================>
#                                      IMPORTS
#<==================================================================================================>
import re
import sys
sys.path.append("../")
from project.models import Investor, Startup
from project.admin.admin_serializer import InvestorSerialize, StartupSerialize


#<==================================================================================================>
#                                  GET USER DETAILS FUNCTION
#<==================================================================================================>
def get_user_data(first_name, last_name, is_inv):
    collection = Investor if is_inv else Startup
    serialise_collection = InvestorSerialize if is_inv else StartupSerialize

    user_obj = None
    first_name = first_name.strip()
    last_name = last_name.strip()
    fn_regex = re.compile(f".*{first_name}.*", re.IGNORECASE)
    ln_regex = re.compile(f".*{last_name}.*", re.IGNORECASE)

    if first_name and last_name:
        user_obj = collection.objects(first_name=fn_regex, last_name=ln_regex).limit(20)
    elif first_name:
        user_obj = collection.objects(first_name=fn_regex).limit(20)
    elif last_name:
        user_obj = collection.objects(last_name=ln_regex).limit(20)

    if not user_obj:
        return {"result": False, "data": None}

    ma_ser = serialise_collection()
    ser_data = ma_ser.dump(user_obj, many=True)
    return {"result": True, "data": ser_data}


#<==================================================================================================>
#                                  GET COMPANY DETAILS FUNCTION
#<==================================================================================================>
def get_company_data(company_name):
    collection = Startup
    serialise_collection = StartupSerialize

    company_name = company_name.strip()
    cn_regex = re.compile(f".*{company_name}.*", re.IGNORECASE)
    user_obj = collection.objects(company_name=cn_regex).limit(20)

    if not user_obj:
        return {"result": False, "data": None}

    ma_ser = serialise_collection()
    ser_data = ma_ser.dump(user_obj, many=True)
    return {"result": True, "data": ser_data}