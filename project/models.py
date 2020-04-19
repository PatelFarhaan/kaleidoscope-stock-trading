import datetime
from flask_login import UserMixin
from project import db, login_manager


@login_manager.user_loader
def user_load(user_id):
    return AdminPortal.objects.get(pk=user_id)


class AdminPortal(db.Document, UserMixin):
    password = db.StringField()
    email = db.EmailField(required=True, unique=True)
    created = db.DateTimeField(default=datetime.datetime.utcnow())

    meta = dict(indexes=['email'])


class Investor(db.Document, UserMixin):
    bio = db.StringField()
    deals = db.StringField()
    sectors = db.ListField()
    angel = db.BooleanField()
    syndicate = db.ListField()
    location = db.StringField()
    password = db.StringField()
    referred_to = db.ListField()
    referred_by = db.EmailField()
    accreditation = db.StringField()
    profile_pic_link = db.StringField()
    password_reset_meta_data = db.DictField()
    approved = db.BooleanField(default=False)
    last_name = db.StringField(max_length=70)
    first_name = db.StringField(max_length=70)
    is_logged_in = db.BooleanField(defalut=False)
    email_confirmed = db.BooleanField(default=False)
    is_google_signup = db.BooleanField(default=False)
    email = db.EmailField(required=True, unique=True)
    first_dashboard_visit = db.BooleanField(default=True)
    created = db.DateTimeField(default=datetime.datetime.utcnow())

    meta = dict(indexes=['email', '-created', 'is_google_signup'])


class Startup(db.Document, UserMixin):
    bio = db.StringField()
    sectors = db.ListField()
    raised = db.StringField()
    progress = db.ListField()
    position = db.StringField()
    password = db.StringField()
    location = db.StringField()
    referred_to = db.ListField()
    slide_deck = db.StringField()
    referred_by = db.EmailField()
    round_size = db.StringField()
    company_link = db.StringField()
    company_name = db.StringField()
    num_team_members = db.IntField()
    startup_pitch = db.StringField()
    profile_pic_link = db.StringField()
    raised_capital_desc = db.StringField()
    password_reset_meta_data = db.DictField()
    approved = db.BooleanField(default=False)
    last_name = db.StringField(max_length=70)
    first_name = db.StringField(max_length=70)
    is_logged_in = db.BooleanField(defalut=False)
    email_confirmed = db.BooleanField(default=False)
    is_google_signup = db.BooleanField(default=False)
    email = db.EmailField(required=True, unique=True)
    first_dashboard_visit = db.BooleanField(default=True)
    created = db.DateTimeField(default=datetime.datetime.utcnow())

    meta = dict(indexes=['email', '-created', 'is_google_signup'])