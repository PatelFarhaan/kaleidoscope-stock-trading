#<==================================================================================================>
#                                              IMPORTS
#<==================================================================================================>
import sys
sys.path.append("../")
from datetime import datetime, timedelta
from project.models import (InvUniqueUsersDaily, StrDailyNewUsers, InvDailyNewUsers, InvWeeklyNewUsers,
                            InvUniqueUsersWeekly, InvUniqueUsersMonthly, StrUniqueUsersDaily,
                            InvMonthlyNewUsers, StrWeeklyNewUsers, StrMonthlyNewUsers,
                            StrUniqueUsersWeekly, StrUniqueUsersMonthly, StrRetention,
                            InvRetention)


#<==================================================================================================>
#                                          ALL ANALYTICS
#<==================================================================================================>
def complete_analytics():
    #<============================== *** New Daily Inv *** =====================================>
    inv_daily_new_obj = InvDailyNewUsers.objects.filter(current=True).first()
    inv_daily_new_count = inv_daily_new_obj.count if inv_daily_new_obj else 0

    inv_weekly_new_obj = InvWeeklyNewUsers.objects.filter(current=True).first()
    inv_weekly_new_count = inv_weekly_new_obj.count if inv_weekly_new_obj else 0

    inv_monthly_new_obj = InvMonthlyNewUsers.objects.filter(current=True).first()
    inv_monthly_new_count = inv_monthly_new_obj.count if inv_monthly_new_obj else 0

    #<============================== *** New Daily Str *** =====================================>
    str_daily_new_obj = StrDailyNewUsers.objects.filter(current=True).first()
    str_daily_new_count = str_daily_new_obj.count if str_daily_new_obj else 0

    str_weekly_new_obj = StrWeeklyNewUsers.objects.filter(current=True).first()
    str_weekly_new_count = str_weekly_new_obj.count if str_weekly_new_obj else 0

    str_monthly_new_obj = StrMonthlyNewUsers.objects.filter(current=True).first()
    str_monthly_new_count = str_monthly_new_obj.count if str_monthly_new_obj else 0

    #<============================== *** Unique Daily Inv *** =====================================>
    inv_daily_unique_obj = InvUniqueUsersDaily.objects.filter(current=True).first()
    inv_daily_unique_count = inv_daily_unique_obj.count if inv_daily_unique_obj else 0

    inv_weekly_unique_obj = InvUniqueUsersWeekly.objects.filter(current=True).first()
    inv_weekly_unique_count = inv_weekly_unique_obj.count if inv_weekly_unique_obj else 0

    inv_monthly_unique_obj = InvUniqueUsersMonthly.objects.filter(current=True).first()
    inv_monthly_unique_count = inv_monthly_unique_obj.count if inv_monthly_unique_obj else 0

    #<============================== *** Unique Daily Str *** =====================================>
    str_daily_unique_obj = StrUniqueUsersDaily.objects.filter(current=True).first()
    str_daily_unique_count = str_daily_unique_obj.count if str_daily_unique_obj else 0

    str_weekly_unique_obj = StrUniqueUsersWeekly.objects.filter(current=True).first()
    str_weekly_unique_count = str_weekly_unique_obj.count if str_weekly_unique_obj else 0

    str_monthly_unique_obj = StrUniqueUsersMonthly.objects.filter(current=True).first()
    str_monthly_unique_count = str_monthly_unique_obj.count if str_monthly_unique_obj else 0

    # <============================= *** Retention and Churn *** ====================================>
    inv_ret_obj = InvRetention.objects.all()[0]
    str_ret_obj = StrRetention.objects.all()[0]

    inv_daily_retention, inv_daily_churn = churn_and_retention(inv_ret_obj.daily, 1)
    inv_weekly_retention, inv_weekly_churn = churn_and_retention(inv_ret_obj.weekly, 7)
    inv_monthly_retention, inv_monthly_churn = churn_and_retention(inv_ret_obj.monthly, 30)
    str_daily_retention, str_daily_churn = churn_and_retention(str_ret_obj.daily, 1)
    str_weekly_retention, str_weekly_churn = churn_and_retention(str_ret_obj.weekly, 7)
    str_monthly_retention, str_monthly_churn = churn_and_retention(inv_ret_obj.monthly, 30)

    data = {}
    data["inv_daily_new_users"] = inv_daily_new_count
    data["inv_weekly_new_users"] = inv_weekly_new_count
    data["inv_monthly_new_users"] = inv_monthly_new_count
    data["str_daily_new_users"] = str_daily_new_count
    data["str_weekly_new_users"] = str_weekly_new_count
    data["str_monthly_new_users"] = str_monthly_new_count

    data["inv_daily_unique_users"] = inv_daily_unique_count
    data["inv_weekly_unique_users"] = inv_weekly_unique_count
    data["inv_monthly_unique_users"] = inv_monthly_unique_count
    data["str_daily_unique_users"] = str_daily_unique_count
    data["str_weekly_unique_users"] = str_weekly_unique_count
    data["str_monthly_unique_users"] = str_monthly_unique_count

    data["inv_daily_retention"] = inv_daily_retention
    data["inv_weekly_retention"] = inv_weekly_retention
    data["inv_monthly_retention"] = inv_monthly_retention
    data["str_daily_retention"] = str_daily_retention
    data["str_weekly_retention"] = str_weekly_retention
    data["str_monthly_retention"] = str_monthly_retention

    data["inv_daily_churn"] = inv_daily_churn
    data["inv_weekly_churn"] = inv_weekly_churn
    data["inv_monthly_churn"] = inv_monthly_churn
    data["str_daily_churn"] = str_daily_churn
    data["str_weekly_churn"] = str_weekly_churn
    data["str_monthly_churn"] = str_monthly_churn
    return data


#<==================================================================================================>
#                                      USER RETENTION
#<==================================================================================================>
def churn_and_retention(retention_list, days):
    if len(retention_list) > 1:
        current = retention_list[-1].get("unique_login")
        _previous = retention_list[-2].get("unique_login")

        # 1 when previous data is not available
        previous = _previous if consecutive_check(retention_list[-1], retention_list[-2], days) else 1
        formula = (current/previous)
        retention = formula * 100
        churn = (1 - formula) * 100
        return f"{retention:.2f}%", f"{churn:.2f}%"
    else:
        return "-", "-"


#<==================================================================================================>
#                                     CONSECUTIVE CHECK
#<==================================================================================================>
def consecutive_check(current, previous, days):
    current = current.get("date")
    previous = previous.get("date")
    return str(datetime.strptime(current, '%Y-%m-%d').date() - timedelta(days=days)) == previous