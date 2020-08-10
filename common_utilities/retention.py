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
    total_count = collection.objects.count()
    resp = collection.objects.skip(int(offset)).limit(10)
    if resp:
        for user in resp:
            temp_obj = {}
            temp_obj["email"] = user.email
            temp_obj["last_login"] = last_login_data(user)
            temp_obj["today"] = True if user.today else False
            temp_obj["first_week"] = True if user.first_week else False
            temp_obj["third_week"] = True if user.third_week else False
            temp_obj["second_week"] = True if user.second_week else False
            temp_obj["fourth_week"] = True if user.fourth_week else False
            res.append(temp_obj)
        return {"result": True, "data": res, "total_count": total_count}
    else:
        res = {}
        res["data"] = None
        res["result"] = False
        res["total_count"] = 0
        return res


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
    res["last_login"] = last_login_data(user)
    res["today"] = True if user.today else False
    res["first_week"] = True if user.first_week else False
    res["third_week"] = True if user.third_week else False
    res["second_week"] = True if user.second_week else False
    res["fourth_week"] = True if user.fourth_week else False
    print(res)
    return {"result": True, "data": res}


#<==================================================================================================>
#                                  USER LAST LOGIN DATA
#<==================================================================================================>
def last_login_data(user_obj: object):
    if user_obj.today:
        last_login = user_obj.today[-1]
        return last_login.strftime(format='%d %b %Y - %H:%M')
    elif user_obj.first_week:
        last_login = user_obj.first_week[-1]
        return last_login.strftime(format='%d %b %Y - %H:%M')
    elif user_obj.second_week:
        last_login = user_obj.second_week[-1]
        return last_login.strftime(format='%d %b %Y - %H:%M')
    elif user_obj.third_week:
        last_login = user_obj.third_week[-1]
        return last_login.strftime(format='%d %b %Y - %H:%M')
    elif user_obj.fourth_week:
        last_login = user_obj.fourth_week[-1]
        return last_login.strftime(format='%d %b %Y - %H:%M')
    return "No Data"


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