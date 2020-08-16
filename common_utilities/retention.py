#<==================================================================================================>
#                                       IMPORTS
#<==================================================================================================>
import sys
sys.path.append("../")
from datetime import datetime, timedelta
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
            temp_obj["last_login"] = user.last_login.strftime('%d %b %Y')
            temp_obj["daily_ret"], temp_obj["daily_churn"] = churn_and_retention(user.daily, 1)
            temp_obj["weekly_ret"], temp_obj["weekly_churn"] = churn_and_retention(user.daily, 7)
            temp_obj["monthly_ret"], temp_obj["monthly_churn"] = churn_and_retention(user.daily, 30)
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
        return {"result": False, "error": "user retention data not available for this user"}

    temp_obj = {}
    temp_obj["email"] = user.email
    temp_obj["last_login"] = user.last_login.strftime('%d %b %Y')
    temp_obj["daily_ret"], temp_obj["daily_churn"] = churn_and_retention(user.daily, 1)
    temp_obj["weekly_ret"], temp_obj["weekly_churn"] = churn_and_retention(user.daily, 7)
    temp_obj["monthly_ret"], temp_obj["monthly_churn"] = churn_and_retention(user.daily, 30)
    return {"result": True, "data": temp_obj}


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
#                                      USER RETENTION
#<==================================================================================================>
def churn_and_retention(retention_list, days):
    if len(retention_list) > 1:
        is_consecutive = consecutive_check(retention_list[-1], retention_list[-2], days)
        if is_consecutive:
            return f"100%", f"100%"
        else:
            return "0%", "0%"
    else:
        return "0%", "0%"


#<==================================================================================================>
#                                     CONSECUTIVE CHECK
#<==================================================================================================>
def consecutive_check(current, previous, days):
    current = current.get("date")
    previous = previous.get("date")
    return str(datetime.strptime(current, '%Y-%m-%d').date() - timedelta(days=days)) == previous