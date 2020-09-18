#<==================================================================================================>
#                                         IMPORTS
#<==================================================================================================>
from flask import Flask
from flask_login import LoginManager
from common_utilities import CONSTANT
from flask_mongoengine import MongoEngine
from flask_marshmallow import Marshmallow


#<==================================================================================================>
#                                     APPLICATION CONFIG
#<==================================================================================================>
app = Flask(__name__)
app.config['SECRET_KEY'] = CONSTANT.SECRET_KEY.value
app.config['MONGODB_SETTINGS'] = {'host': CONSTANT.CURRENT_DATABASE.value}

db = MongoEngine(app)
ma = Marshmallow(app)

login_manager = LoginManager(app)
login_manager.login_view = "trade.login"


#<==================================================================================================>
#                                    ADMIN PANEL BLUEPRINT
#<==================================================================================================>
from project.trade.views import trade_blueprint
from project.error.error_handler import errorpage_blueprint

app.register_blueprint(trade_blueprint)
app.register_blueprint(errorpage_blueprint)