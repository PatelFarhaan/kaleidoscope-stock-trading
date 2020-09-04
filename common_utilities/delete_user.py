#<==================================================================================================>
#                                      IMPORTS
#<==================================================================================================>
import sys
sys.path.append('../')
from project.models import Investor, Startup


#<==================================================================================================>
#                                   DELETE A USER
#<==================================================================================================>
def delete_a_user(email, is_inv):
    collection = Investor if is_inv else Startup
    user_obj = collection.objects.filter(email=email).first()
    if user_obj:
        user_obj.delete()
        return {"result": True, "error": "user delete successfully"}
    else:
        return {"result": False, "error": "user does not exist"}