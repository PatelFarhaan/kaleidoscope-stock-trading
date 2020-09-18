import sys
sys.path.append("../")
from project.models import Shares


def shares_test_data_populate():
    share_names = ["SPY Equity", "QQQ Equity", "HYG Equity"]
    available_shares = [500] * len(share_names)

    for k, v in zip(share_names, available_shares):
        new_shares = Shares(share_name=k,
                            available_number=v)
        new_shares.save()