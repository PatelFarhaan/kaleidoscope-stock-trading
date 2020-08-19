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
def list_equal_len_checker(arr1, arr2, arr3):
    _min_len = min(len(arr1), len(arr2), len(arr3))
    if len(arr1) > _min_len:
        arr1 = arr1[:_min_len]

    if len(arr2) > _min_len:
        arr2 = arr2[:_min_len]

    if len(arr3) > _min_len:
        arr3 = arr3[:_min_len]

    print(len(arr1), len(arr2), len(arr3))
    return arr1, arr2, arr3


#<==================================================================================================>
#                                          SIGNUP GRPAHS
#<==================================================================================================>
def helper_function(inv_collection, str_collection):

    inv_data = inv_collection.objects.order_by('-id').limit(30)
    inv_count = [i.count for i in inv_data]
    dates = [i.current_dt.strftime('%d %b %Y')[:-2] for i in inv_data]

    str_data = str_collection.objects.order_by('-id').limit(30)
    str_count = [i.count for i in str_data]
    return dates[::-1], inv_count[::-1], str_count[::-1]


#<==================================================================================================>
#                                      USER RETENTION
#<==================================================================================================>
def retention_calculation(retention_list, days):
    dates = []
    ret_data = []

    for i in range(len(retention_list)):
        data_chunk = retention_list[i : i+2]
        if len(data_chunk) == 2:
            current = data_chunk[-1].get("unique_login")
            _previous = data_chunk[-2].get("unique_login")

            previous = _previous if consecutive_check(data_chunk[-1], data_chunk[-2], days) else 1
            formula = (current / previous)
            retention = formula
            dates.append(data_chunk[-1].get("date")[2:])
            ret_data.append(float(f"{retention:.2f}"))
    return dates, ret_data


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
def signup_graph(path):

    dates, inv_count, str_count = helper_function(InvDailyNewUsers, StrDailyNewUsers)
    dates, inv_ret_data, str_ret_data = list_equal_len_checker(dates, inv_count,
                                                               str_count)

    plt.plot(dates, inv_ret_data, color='green', linestyle='dashed', linewidth = 3,
             marker='o', markerfacecolor='blue', markersize=12)
    plt.plot(dates, str_ret_data, color='red', linestyle='dashed', linewidth = 3,
             marker='o', markerfacecolor='blue', markersize=12)

    plt.xlabel('Date')
    plt.ylabel('Users')
    fig = plt.gcf()
    fig.set_size_inches(14, 5)

    plt.title('New Signup Graphs')
    plt.savefig(f'{path}/signup_graph.png', dpi=100)
    plt.close()
    return


#<==================================================================================================>
#                                           UNIQUE USERS GRPAHS
#<==================================================================================================>
def unique_user_graph(path):
    dates, inv_count, str_count = helper_function(InvUniqueUsersDaily, StrUniqueUsersDaily)
    dates, inv_ret_data, str_ret_data = list_equal_len_checker(dates, inv_count,
                                                               str_count)

    plt.plot(dates, inv_ret_data, color='green', linestyle='dashed', linewidth = 3,
             marker='o', markerfacecolor='blue', markersize=12)
    plt.plot(dates, str_ret_data, color='red', linestyle='dashed', linewidth = 3,
             marker='o', markerfacecolor='blue', markersize=12)

    plt.xlabel('Date')
    plt.ylabel('Users')
    fig = plt.gcf()
    fig.set_size_inches(14, 5)

    plt.title('Active User Graphs')
    plt.savefig(f'{path}/unique_user_graph.png')
    plt.close()
    return


#<==================================================================================================>
#                                  RETENTION AND CHURN GRAPHS
#<==================================================================================================>
def retention_graph(path):
    inv_obj = InvRetention.objects.all()[0]
    str_obj = StrRetention.objects.all()[0]
    dates, inv_ret_data = retention_calculation(inv_obj.daily[-31::], 1)
    dates, str_ret_data = retention_calculation(str_obj.daily[-31::], 1)
    dates, inv_ret_data, str_ret_data = list_equal_len_checker(dates, inv_ret_data,
                                                               str_ret_data)


    ##############################################################################
    plt.plot(dates, inv_ret_data, color='green', linestyle='dashed', linewidth = 3,
             marker='o', markerfacecolor='blue', markersize=12)
    plt.plot(dates, str_ret_data, color='red', linestyle='dashed', linewidth = 3,
             marker='o', markerfacecolor='blue', markersize=12)

    plt.xlabel('Date')
    plt.ylabel('Users')
    fig = plt.gcf()
    fig.set_size_inches(14, 5)

    plt.title('Retention Overview')
    plt.savefig(f'{path}/retention_graph.png')
    plt.close()
    return


#<==================================================================================================>
#                                          RUN ALL FUNCTIONS
#<==================================================================================================>
def run_all():
    localhost = "/Users/farhaan/projects/admin/project/static/graphs"
    server = "/home/ubuntu/admin/project/static/graphs"
    path = server
    signup_graph(path)
    retention_graph(path)
    unique_user_graph(path)