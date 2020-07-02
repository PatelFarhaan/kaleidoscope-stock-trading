#<==================================================================================================>
#                                      IMPORTS
#<==================================================================================================>
from project import ma


#<==================================================================================================>
#                                      INVESTOR ML SCHEMA
#<==================================================================================================>
class InvestorMLSchema(ma.Schema):
    class Meta:
        fields = ("count_invited", "count_passed", "invite_accepted_notify", "all_transaction_fields",
                  "first_dashboard_visit", "created", "investor", "show_profile", "monday_notifications",
                  "profile_pic_link", "password_reset_meta_data", "approved", "first_invite", "last_name",
                  "matched_week", "prior_investments", "connected", "passed", "pending", "delete_account",
                  "bio", "deals", "sectors", "angel", "syndicate", "location", "password", "accreditation",
                  "first_name", "is_logged_in", "email_confirmed", "is_google_signup", "email", "show_limit")


#<==================================================================================================>
#                                      INVESTOR STR SCHEMA
#<==================================================================================================>
class StartupMLSchema(ma.Schema):
    class Meta:
        fields = ("slide_deck", "round_size", "company_link", "company_name", "num_team_members",
                  "last_name", "first_name", "is_logged_in", "email_confirmed", "is_google_signup", "email",
                  "bio", "sectors", "raised", "progress", "position", "password", "location", "first_invite",
                  "count_invited", "count_passed", "show_limit", "invite_accepted_notify", "all_transaction_fields",
                  "first_dashboard_visit", "created", "investor", "feedback", "connected", "passed", "matched_week",
                  "startup_pitch", "profile_pic_link", "raised_capital_desc", "password_reset_meta_data", "approved",
                  "pending", "co_founders", "show_slide_deck", "delete_account", "show_profile", "monday_notification")