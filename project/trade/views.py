#<==================================================================================================>
#                                       IMPORTS
#<==================================================================================================>
from common_utilities.blotter import Blotter
from werkzeug.security import check_password_hash
from project.trade.serializer import SharesSchema
from project.models import User, Shares, Transaction
from werkzeug.security import generate_password_hash
from flask_login import login_required, login_user, logout_user
from flask import Blueprint, render_template, request, redirect, url_for, flash, session


#<==================================================================================================>
#                                       TRADE BLUEPRINT
#<==================================================================================================>
trade_blueprint = Blueprint('trade', '__name__', template_folder='templates',
                            static_folder='static')


#<==================================================================================================>
#                                         LOGIN
#<==================================================================================================>
@trade_blueprint.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        required = (email, password)
        if not all(required):
            return render_template('login.html', res={"result": False,
                                                      "message": "Email and Password are Manditory"})

        user_obj = User.objects.filter(email=email).first()
        if not user_obj:
            return render_template('login.html', res={"result": False, "message": "Wrong Credentials"})

        if check_password_hash(user_obj.password, password):
            login_user(user_obj)
            session["email"] = email
            return redirect(url_for('trade.trade_function'))
        return render_template('login.html', res={"result": False, "message": "Wrong Credentials"})

    elif request.method == "GET":
        return render_template("login.html")


#<==================================================================================================>
#                                       LOGOUT
#<==================================================================================================>
@trade_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("user logged out successfully!!!")
    return redirect(url_for("trade.login"))


#<==================================================================================================>
#                                  TRADE FUNCTIONALITY
#<==================================================================================================>
@trade_blueprint.route('/trade-blotter', methods=["GET", "POST"])
@login_required
def trade_function():
    if request.method == "GET":
        # user object
        user_obj = User.objects.filter(email=session["email"]).first()
        if not user_obj:
            flash("Some error encountered. Please login again")
            return redirect(url_for("trade.trade_function"))

        available_shares = Shares.objects.all()
        ma_schema = SharesSchema()
        resp = ma_schema.dump(available_shares, many=True)

        transaction_obj = Transaction.objects.filter(email=session["email"]).all()
        transaction_obj = [ {"email": ele.email,
                              "date": ele.date,
                              "side": ele.side,
                              "ticker": ele.ticker,
                              "trader": ele.trader,
                              "share_number": ele.share_number} for ele in transaction_obj ]
        return render_template('index.html', available_shares=resp, users_shares=user_obj.share_holding,
                               transaction_obj=transaction_obj)

    elif request.method == "POST":
        # Entire Traders

        side = request.form.get("side")
        date = request.form.get("date")
        trader = request.form.get("trader")
        ticker = request.form.get("ticker")
        order_type = request.form.get("order_type")
        order_value = int(request.form.get("order_value"))

        kwargs_obj = {"side": side, "date": date, "trader": trader, "ticker": ticker,
                      "order_type": order_type, "number": order_value}

        # user object
        user_obj = User.objects.filter(email=session["email"]).first()
        if not user_obj:
            flash("Some error encountered. Please login again")
            return redirect(url_for("trade.trade_function"))

        # blotter object
        blotter_obj = Blotter(trader, user_obj)

        share_information = blotter_obj.shares_information(ticker)
        if not share_information.get("result"):
            flash(share_information.get("message"))
            return redirect(url_for("trade.trade_function"))

        available_shares = share_information.get("data")

        if order_type == "Position in %":
            order_value = int( (available_shares * int(order_value)) // 100 )
            kwargs_obj["number"] = order_value

        if side == "Buy" and order_value > available_shares:
            flash(f"{order_value} {ticker} not available")
            return redirect(url_for("trade.trade_function"))

        resp = blotter_obj.post_transaction(kwargs_obj)
        if not resp.get("message"):
            flash("Transaction Successfull")
        else:
            flash(resp.get("message"))
        return redirect(url_for("trade.trade_function"))


#<==================================================================================================>
#                                       REGISTER
#<==================================================================================================>
@trade_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        required = (email, password, confirm_password)
        if not all(required):
            return render_template('register.html', res={"result": False,
                                                      "message": "All fields are Manditory"})

        if password != confirm_password:
            return render_template('register.html', res={"result": False,
                                                      "message": "Passwords do not match"})

        user_obj = User.objects.filter(email=email).first()

        if user_obj:
            return render_template('register.html', res={"result": False, "message": "User Exists"})

        req = {"email": email, "password": generate_password_hash(password), }
        # noinspection PyArgumentList
        new_user = User(**req)
        new_user.save()
        flash("User created successfully. Please login to continue.")
        return redirect(url_for("trade.login"))



    elif request.method == "GET":
        return render_template("register.html")