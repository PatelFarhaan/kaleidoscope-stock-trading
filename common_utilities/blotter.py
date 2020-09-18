import sys
sys.path.append("../")
from project.models import Shares, Transaction


class Blotter(object):
    def __init__(self, trader, user_obj):
        self.trader = trader
        self.user = user_obj
        self.share_model = Shares
        self.transaction_model = Transaction


    def shares_information(self, share_name):
        share_obj = self.share_model.objects.filter(share_name=share_name).first()
        if not share_obj:
            return {"result": False, "message": "Share does not exist"}
        return {"result": True, "message": "Share exists", "data": share_obj.available_number}


    def post_transaction(self, kwargs):
        date = kwargs.get("date")
        _action = kwargs.get("side")
        share_name = kwargs.get("ticker")
        no_of_shares = kwargs.get("number")

        shares_obj = self.share_model.objects.filter(share_name=share_name).first()
        available_shares = shares_obj.available_number
        user_shares = dict(self.user.share_holding)

        if _action == "Buy":

            if not user_shares.get(share_name):
                user_shares[share_name] = no_of_shares
            else:
                user_shares[share_name] += no_of_shares

            # Updating number of shares
            available_shares -= no_of_shares

        elif _action == "Sell":
            if not user_shares.get(share_name):
                return {"result": False, "message": "you do not have this share"}

            user_share_amt = user_shares.get(share_name)
            if user_share_amt < no_of_shares:
                return {"result": False, "message": "you do not have enough share"}

            user_shares[share_name] -= no_of_shares

            # Updating number of shares
            available_shares += no_of_shares

        # creating a new transaction
        new_transaction_obj = self.transaction_model(date=date, side=_action, ticker=share_name,
                                                     email=self.user.email, trader=self.trader, share_number=no_of_shares)
        new_transaction_obj.save()
        shares_obj.available_number = available_shares
        shares_obj.save()
        self.user.share_holding = dict(user_shares)
        self.user.save()
        return {"result": True}