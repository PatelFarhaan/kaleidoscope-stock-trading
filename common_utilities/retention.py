#<==================================================================================================>
#                                       IMPORTS
#<==================================================================================================>
import sys
sys.path.append("../")
from project.models import InvestorUserAnalytics, StartupUserAnalytics


#<==================================================================================================>
#                                  GENERIC HELPER FUNCTION
#<==================================================================================================>
def helper_function(collection: (InvestorUserAnalytics, StartupUserAnalytics),
                    page_no=0):
    res = []
    offset = int(page_no) * 10
    resp = collection.objects.skip(int(offset)).limit(10)
    for user in resp:
        temp_obj = {}
        temp_obj["email"] = user.email
        temp_obj["today"] = True if user.today else False
        temp_obj["first_week"] = True if user.first_week else False
        temp_obj["third_week"] = True if user.third_week else False
        temp_obj["second_week"] = True if user.second_week else False
        temp_obj["fourth_week"] = True if user.fourth_week else False
        res.append(temp_obj)
    return {"result": True, "data": res}

#<==================================================================================================>
#                                    COMPLETE STARTUP RETENTION
#<==================================================================================================>
def startup_retention(page_no):
    return helper_function(StartupUserAnalytics, page_no)


#<==================================================================================================>
#                                    COMPLETE INVESTOR RETENTION
#<==================================================================================================>
def investor_retention(page_no):
    return helper_function(InvestorUserAnalytics, page_no)


#<==================================================================================================>
#                                    SINGLE USER RETENTION
#<==================================================================================================>
def user_retention(email, is_inv):
    collection = InvestorUserAnalytics if is_inv else StartupUserAnalytics
    user = collection.objects.filter(email=email).first()
    if not user:
        return {"result": False, "error": "user retention data not available"}

    res = {}
    res["email"] = user.email
    res["today"] = True if user.today else False
    res["first_week"] = True if user.first_week else False
    res["third_week"] = True if user.third_week else False
    res["second_week"] = True if user.second_week else False
    res["fourth_week"] = True if user.fourth_week else False
    return {"result": True, "data": res}