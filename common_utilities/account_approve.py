#<==================================================================================================>
#                                       IMPORTS
#<==================================================================================================>
import sys
import threading
sys.path.append("../")
from flask import redirect, url_for
from project.models import Investor, Startup
from common_utilities.wait_list_completed_startup import wait_list_over_str
from common_utilities.wait_list_completed_investor import wait_list_over_inv


#<==================================================================================================>
#                                  ACCOUNT APPROVE: INV + STR
#<==================================================================================================>
def approve_account(user_email, is_inv):
    collection = Investor if is_inv else Startup
    email_target = wait_list_over_inv if is_inv else wait_list_over_str
    redirect_url = 'admin.investor_account' if is_inv else 'admin.startup_account'

    user_obj = collection.objects.filter(email=user_email).first()
    if not user_obj:
        return redirect(url_for(redirect_url))

    user_obj.approved = True
    user_obj.save()

    email, first_name = user_obj.email, user_obj.first_name
    thread = threading.Thread(target=email_target, args=(email, first_name,))
    thread.start()