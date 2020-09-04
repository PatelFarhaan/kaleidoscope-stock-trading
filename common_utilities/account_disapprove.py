#<==================================================================================================>
#                                       IMPORTS
#<==================================================================================================>
import sys
sys.path.append("../")
from flask import redirect, url_for
from project.models import Investor, Startup


#<==================================================================================================>
#                                  ACCOUNT DIS-APPROVE: INV + STR
#<==================================================================================================>
def disapprove_account(user_email, is_inv):
    collection = Investor if is_inv else Startup
    redirect_url = 'admin.investor_account' if is_inv else 'admin.startup_account'

    user_obj = collection.objects.filter(email=user_email).first()
    if not user_obj:
        return redirect(url_for(redirect_url))

    user_obj.approved = False
    user_obj.save()