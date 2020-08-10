#<==================================================================================================>
#                                       IMPORTS
#<==================================================================================================>
import sys
sys.path.append("../")
from project.models import (InvUniqueUsersDaily, StrDailyNewUsers, InvDailyNewUsers, InvWeeklyNewUsers,
                            InvMonthlyNewUsers, StrWeeklyNewUsers, StrMonthlyNewUsers,
                            InvUniqueUsersWeekly, InvUniqueUsersMonthly, StrUniqueUsersDaily,
                            StrUniqueUsersWeekly, StrUniqueUsersMonthly)


#<==================================================================================================>
#                                  ALL ANALYTICS
#<==================================================================================================>
def complete_analytics():
    inv_daily_new_obj = InvDailyNewUsers.objects.filter(current=True).first()
    inv_daily_new_count = inv_daily_new_obj.count if inv_daily_new_obj else 0

    inv_weekly_new_obj = InvWeeklyNewUsers.objects.filter(current=True).first()
    inv_weekly_new_count = inv_weekly_new_obj.count if inv_weekly_new_obj else 0

    inv_monthly_new_obj = InvMonthlyNewUsers.objects.filter(current=True).first()
    inv_monthly_new_count = inv_monthly_new_obj.count if inv_monthly_new_obj else 0


    str_daily_new_obj = StrDailyNewUsers.objects.filter(current=True).first()
    str_daily_new_count = str_daily_new_obj.count if str_daily_new_obj else 0

    str_weekly_new_obj = StrWeeklyNewUsers.objects.filter(current=True).first()
    str_weekly_new_count = str_weekly_new_obj.count if str_weekly_new_obj else 0

    str_monthly_new_obj = StrMonthlyNewUsers.objects.filter(current=True).first()
    str_monthly_new_count = str_monthly_new_obj.count if str_monthly_new_obj else 0

    inv_daily_unique_obj = InvUniqueUsersDaily.objects.filter(current=True).first()
    inv_daily_unique_count = inv_daily_unique_obj.count if inv_daily_unique_obj else 0

    inv_weekly_unique_obj = InvUniqueUsersWeekly.objects.filter(current=True).first()
    inv_weekly_unique_count = inv_weekly_unique_obj.count if inv_weekly_unique_obj else 0

    inv_monthly_unique_obj = InvUniqueUsersMonthly.objects.filter(current=True).first()
    inv_monthly_unique_count = inv_monthly_unique_obj.count if inv_monthly_unique_obj else 0

    str_daily_unique_obj = StrUniqueUsersDaily.objects.filter(current=True).first()
    str_daily_unique_count = str_daily_unique_obj.count if str_daily_unique_obj else 0

    str_weekly_unique_obj = StrUniqueUsersWeekly.objects.filter(current=True).first()
    str_weekly_unique_count = str_weekly_unique_obj.count if str_weekly_unique_obj else 0

    str_monthly_unique_obj = StrUniqueUsersMonthly.objects.filter(current=True).first()
    str_monthly_unique_count = str_monthly_unique_obj.count if str_monthly_unique_obj else 0


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

    return data