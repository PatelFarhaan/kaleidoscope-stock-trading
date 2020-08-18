#<==================================================================================================>
#                                           IMPORTS
#<==================================================================================================>
import sys
import matplotlib.pyplot as plt
sys.path.append("../")
plt.switch_backend('Agg')
from datetime import datetime, timedelta
from project.models import (InvDailyNewUsers, StrDailyNewUsers, StrUniqueUsersDaily,
                            InvUniqueUsersDaily, InvRetention, StrRetention)


#<==================================================================================================>
#                                          SIGNUP GRPAHS
#<==================================================================================================>
def helper_function(inv_collection, str_collection):

    inv_data = inv_collection.objects.order_by('-id').limit(5)
    inv_count = [i.count for i in inv_data]
    dates = [i.current_dt.strftime('%d %b %Y') for i in inv_data]

    str_data = str_collection.objects.order_by('-id').limit(5)
    str_count = [i.count for i in str_data]
    return dates[::-1], inv_count[::-1], str_count[::-1]


#<==================================================================================================>
#                                      USER RETENTION
#<==================================================================================================>
def retention_calculation(retention_list, days):
    dates = []
    ret_data = []
    churn_data = []

    for i in range(len(retention_list)):
        data_chunk = retention_list[i : i+2]
        if len(data_chunk) == 2:
            current = data_chunk[-1].get("unique_login")
            _previous = data_chunk[-2].get("unique_login")

            previous = _previous if consecutive_check(data_chunk[-1], data_chunk[-2], days) else 1
            formula = (current / previous)
            retention = formula
            churn = (1 - formula)
            dates.append(data_chunk[-1].get("date"))
            ret_data.append(float(f"{retention:.2f}"))
            churn_data.append(float(f"{churn:.2f}"))
    return dates, ret_data, churn_data


#<==================================================================================================>
#                                     CONSECUTIVE CHECK
#<==================================================================================================>
def consecutive_check(current, previous, days):
    current = current.get("date")
    previous = previous.get("date")
    return str(datetime.strptime(current, '%Y-%m-%d').date() - timedelta(days=days)) == previous


#<==================================================================================================>
#                                          SIGNUP GRPAHS
#<==================================================================================================>
def signup_graph():

    dates, inv_count, str_count = helper_function(InvDailyNewUsers, StrDailyNewUsers)

    plt.plot(dates, inv_count, color='green', linestyle='dashed', linewidth = 3,
             marker='o', markerfacecolor='blue', markersize=12)
    plt.plot(dates, str_count, color='red', linestyle='dashed', linewidth = 3,
             marker='o', markerfacecolor='blue', markersize=12)

    plt.xlabel('Date')
    plt.ylabel('Users')

    plt.title('New Signup Graphs')
    plt.savefig('/home/ubuntu/admin/project/static/graphs/signup_graph.png')
    plt.close()
    return


#<==================================================================================================>
#                                           UNIQUE USERS GRPAHS
#<==================================================================================================>
def unique_user_graph():
    dates, inv_count, str_count = helper_function(InvUniqueUsersDaily, StrUniqueUsersDaily)

    plt.plot(dates, inv_count, color='green', linestyle='dashed', linewidth = 3,
             marker='o', markerfacecolor='blue', markersize=12)
    plt.plot(dates, str_count, color='red', linestyle='dashed', linewidth = 3,
             marker='o', markerfacecolor='blue', markersize=12)

    plt.xlabel('Date')
    plt.ylabel('Users')

    plt.title('Active User Graphs')
    plt.savefig('/home/ubuntu/admin/project/static/graphs/unique_user_graph.png')
    plt.close()
    return


#<==================================================================================================>
#                                  RETENTION AND CHURN GRAPHS
#<==================================================================================================>
def retention_graph():
    inv_obj = InvRetention.objects.all()[0]
    str_obj = StrRetention.objects.all()[0]
    dates, inv_ret_data, inv_churn_data = retention_calculation(inv_obj.daily[-6::], 1)
    dates, str_ret_data, str_churn_data = retention_calculation(str_obj.daily[-6::], 1)

    ##############################################################################
    plt.plot(dates, inv_ret_data, color='green', linestyle='dashed', linewidth = 3,
             marker='o', markerfacecolor='blue', markersize=12)
    plt.plot(dates, str_ret_data, color='red', linestyle='dashed', linewidth = 3,
             marker='o', markerfacecolor='blue', markersize=12)

    plt.xlabel('Date')
    plt.ylabel('Users')

    plt.title('Retention Overview')
    plt.savefig('/home/ubuntu/admin/project/static/graphs/retention_graph.png')
    plt.close()
    ##############################################################################

    plt.plot(dates, inv_churn_data, color='green', linestyle='dashed', linewidth = 3,
             marker='o', markerfacecolor='blue', markersize=12)
    plt.plot(dates, str_churn_data, color='red', linestyle='dashed', linewidth = 3,
             marker='o', markerfacecolor='blue', markersize=12)

    _min = min(min(inv_churn_data), min(str_churn_data))
    _max = max(max(inv_churn_data), max(str_churn_data))
    plt.ylim([_min-0.5, _max+0.5])

    plt.xlabel('Date')
    plt.ylabel('Users')

    plt.title('Churn Overview')
    plt.savefig('/home/ubuntu/admin/project/static/graphs/churn_graph.png')
    plt.close()
    ##############################################################################
    return


#<==================================================================================================>
#                                          RUN ALL FUNCTIONS
#<==================================================================================================>
def run_all():
    signup_graph()
    retention_graph()
    unique_user_graph()