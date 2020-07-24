#<==================================================================================================>
#                                      IMPORTS
#<==================================================================================================>
import os
import sys
import uuid
import shutil
import pandas as pd
sys.path.append("../")
from common_utilities.beta_inv_data import investor_beta_data
from common_utilities.strartup_data_populate import startup_data
from common_utilities.investor_data_populate import investor_data


#<==================================================================================================>
#                                  FILE PROCESSING
#<==================================================================================================>
def file_process(file_obj, is_inv, is_beta=False):
    file_name = file_obj.filename.replace(' ', '').split('.', 1)[0]

    file_location = f"{os.getcwd()}/{str(uuid.uuid4())}"
    if os._exists(file_location):
        shutil.rmtree(file_location)

    os.mkdir(file_location)
    with open(f"{file_location}/{file_name}", 'wb') as f:
        f.write(file_obj.read())

    try:
        read_file = pd.read_excel(f'{file_location}/{file_name}')
        file_path = f'{file_location}/{file_name}.csv'
        read_file.to_csv(file_path)
    except:
        return False

    if is_beta:
        if is_inv:
            return investor_beta_data(file_path, file_location)
        else:
            pass
    else:
        if is_inv:
            return investor_data(file_path, file_location)
        else:
            return startup_data(file_path, file_location)