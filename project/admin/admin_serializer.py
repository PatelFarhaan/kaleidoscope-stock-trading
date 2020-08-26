from project import ma
from marshmallow import fields as fb


#<==================================================================================================>
#                               MULTIPLE INVESTOR SERIALIZER
#<==================================================================================================>
class InvestorSerialize(ma.Schema):
    created = fb.DateTime(format='%d %b %Y')

    class Meta:
        strict = True

        fields = ("email", "created", "location", "approved", "first_name",
                  "last_name", "email_confirmed", "profile_pic_link", "syndicate")


#<==================================================================================================>
#                               MULTIPLE STARTUP SERIALIZER
#<==================================================================================================>
class StartupSerialize(ma.Schema):
    created = fb.DateTime(format='%d %b %Y')

    class Meta:
        fields = ("email", "company_name", "created", "approved", "first_name", "email_confirmed",
                  "last_name", "profile_pic_link")


# <==================================================================================================>
#                               SINGLE INVESTOR SERIALIZER
# <==================================================================================================>
class InvestorSerializeSingle(ma.Schema):
    created = fb.DateTime(format='%d %b %Y')

    class Meta:
        fields = ("deals", "angel", "created", "location", "approved", "first_name",
                  "email_confirmed", "bio", "sectors", "syndicate", "accreditation",
                  "profile_pic_link", "last_name", "email", "connected", "prior_investments")



# <==================================================================================================>
#                               SINGLE STARTUP SERIALIZER
# <==================================================================================================>
class StartupSerializeSingle(ma.Schema):
    created = fb.DateTime(format='%d %b %Y')
    class Meta:
        fields = ("bio", "sectors", "raised", "progress", "position", "location", "slide_deck",
                  "round_size", "company_link", "company_name", "num_team_members", "startup_pitch",
                  "profile_pic_link", "raised_capital_desc", "approved", "email_confirmed", "last_name",
                  "first_name", "email", "created", "connected", "co_founders")


# <==================================================================================================>
#                                      INVESTOR STR SCHEMA
# <==================================================================================================>
class InvestorBetaSchema(ma.Schema):
    class Meta:
        fields = ("email", "password", "confirmation_link")