#<==================================================================================================>
#                                       IMPORTS
#<==================================================================================================>
import sys
import string, random
sys.path.append("../")
from project.models import InviteCodes


# <==================================================================================================>
#                                 INVESTOR DISCOVER CARDS DATA DUMP
# <==================================================================================================>
def generate_code():
    invite_code_obj = InviteCodes.objects.all()

    if not invite_code_obj:
        first_code = id_generator({})
        new_obj = InviteCodes(codes={first_code: True})
        new_obj.save()
        return first_code
    else:
        invite_code_obj = invite_code_obj[0]
        existing_codes = dict(invite_code_obj.codes)
        code = id_generator(existing_codes)
        existing_codes[code] = True
        invite_code_obj.codes = existing_codes
        invite_code_obj.save()
        return code


#<==================================================================================================>
#                                 INVESTOR DISCOVER CARDS DATA DUMP
#<==================================================================================================>
def id_generator(existing_codes, size=10, chars=string.ascii_letters + string.digits):
    _temp_code = ''.join(random.choice(chars) for _ in range(size))
    if _temp_code in existing_codes:
        id_generator(existing_codes)
    return _temp_code