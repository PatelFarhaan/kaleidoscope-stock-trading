#<==================================================================================================>
#                                       IMPORTS
#<==================================================================================================>
from werkzeug.security import check_password_hash
from common_utilities.analtics import complete_analytics
from common_utilities.file_processing import file_process
from common_utilities.account_approve import approve_account
from flask_login import login_required, login_user, logout_user
from common_utilities.account_disapprove import disapprove_account
from project.models import Investor, Startup, AdminPortal, InvestorBetaData
from common_utilities.matching_db_updates import update_into_matching, clean_discover
from common_utilities.retention import investor_retention, startup_retention, user_retention
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from project.admin.admin_serializer import (InvestorSerialize, StartupSerialize, InvestorBetaSchema,
                                            StartupSerializeSingle, InvestorSerializeSingle)






#<==================================================================================================>
#                                       ADMIN BLUEPRINT
#<==================================================================================================>
admin_blueprint = Blueprint('admin', '__name__', template_folder='templates',
                            static_folder='static', url_prefix='/admin')


#<==================================================================================================>
#                                      ADMIN PANE LOGIN
#<==================================================================================================>
@admin_blueprint.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        required = (email, password)
        if not all(required):
            return render_template('login.html', res={"result": False,
                                                      "message": "Email and Password are Manditory"})

        admin_obj = AdminPortal.objects.filter(email=email).first()
        if not admin_obj:
            request.path = None
            return render_template('login.html', res={"result": False, "message": "Wrong Credentials"})

        if check_password_hash(admin_obj.password, password):
            login_user(admin_obj)
            return redirect(url_for('admin.investor_account'))
        request.path=None
        return render_template('login.html', res={"result": False, "message": "Wrong Credentials"})

    elif request.method == "GET":
        return render_template("login.html")


#<==================================================================================================>
#                                    ADMIN PANEL LOGOUT
#<==================================================================================================>
@admin_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("user logged out successfully!!!")
    return redirect(url_for("admin.login"))


#<==================================================================================================>
#                          INVESTOR ACCOUNT + PAGINATION + SINGLE USER
#<==================================================================================================>
@admin_blueprint.route('/investor-account', methods=["GET", "POST"])
@login_required
def investor_account():
    def all_inv_data(page_no=0):
        offset = 10 * int(page_no)
        resp = Investor.objects.skip(int(offset)).limit(10)
        ma_ser = InvestorSerialize()
        if resp:
            total_inv_counts = Investor.objects.count()
            res = ma_ser.dump(resp, many=True)
            return_data = {}
            return_data["data"] = res
            return_data["result"] = True
            total_str_counts = Startup.objects.count()
            return_data["total_count_str"] = total_str_counts
            return_data["total_count_inv"] = total_inv_counts
        else:
            return_data = {}
            return_data["data"] = None
            return_data["result"] = False
            return_data["total_count_inv"] = 0
            total_str_counts = Startup.objects.count()
            return_data["total_count_str"] = total_str_counts
        return return_data

    if request.method == "GET":
        return_data = all_inv_data()
        return render_template('investor.html', inv_data=return_data)

    elif request.method == "POST":
        if request.files:
            file_obj = request.files.get('inv_csv')

            if not file_obj:
                return redirect(url_for('admin.investor_account'))

            res = file_process(file_obj, True)
            if res:
                flash("All Investor's updated successfully")
                return redirect(url_for("admin.investor_account"))
            else:
                flash("Some problem occurred while processing the file")
                return redirect(url_for("admin.investor_account"))

        elif request.form.getlist("check"):
            print("here")
            return "jhabsdkjas"

        elif request.form.get('approve'):
            user_email = request.form.get('approve')
            if not user_email:
                return redirect(url_for('admin.investor_account'))
            approve_account(user_email, True)

        elif request.form.get('disapprove'):
            user_email = request.form.get('disapprove')
            if not user_email:
                return redirect(url_for('admin.investor_account'))
            disapprove_account(user_email, True)

        elif request.form.get("page"):
            page_no = request.form.get('page')
            return_data = all_inv_data(page_no)
            return render_template('investor.html', inv_data=return_data)
        return redirect(url_for('admin.investor_account'))


@admin_blueprint.route('/get-single-investor', methods=["POST"])
@login_required
def get_investor_data():
    email = request.form.get('email')
    user_obj = Investor.objects.filter(email=email).first()
    if not user_obj:
        return jsonify({"result": False})

    ma_ser = InvestorSerializeSingle()
    ser_data = ma_ser.dump(user_obj)
    ret_obj = jsonify({"result": True, "data": ser_data})
    ret_obj.headers.add('Access-Control-Allow-Origin', '*')
    return ret_obj


#<==================================================================================================>
#                              STARTUP ACCOUNT + PAGINATION + SINGLE USER
#<==================================================================================================>
@admin_blueprint.route('/startup-account', methods=["GET", "POST"])
@login_required
def startup_account():
    def all_str_data(page_no=0):
        offset = int(page_no) * 10
        resp = Startup.objects.skip(int(offset)).limit(10)
        ma_ser = StartupSerialize()
        if resp:
            total_str_counts = Startup.objects.count()
            res = ma_ser.dump(resp, many=True)
            return_data = {}
            return_data["data"] = res
            return_data["result"] = True
            total_inv_counts = Investor.objects.count()
            return_data["total_count_str"] = total_str_counts
            return_data["total_count_inv"] = total_inv_counts
        else:
            return_data = {}
            return_data["data"] = None
            return_data["result"] = False
            return_data["total_count_str"] = 0
            total_inv_counts = Investor.objects.count()
            return_data["total_count_inv"] = total_inv_counts
        return return_data

    if request.method == "GET":
        return_data = all_str_data()
        return render_template('startup.html', inv_data=return_data)

    elif request.method == "POST":
        if request.files:
            file_obj = request.files.get('str_csv')

            if not file_obj:
                return redirect(url_for('admin.startup_account'))

            res = file_process(file_obj, False)
            if res:
                flash("All Startup's updated successfully")
                return redirect(url_for("admin.startup_account"))
            else:
                flash("Some problem occurred while processing the file")
                return redirect(url_for("admin.startup_account"))

        if request.form.get('approve'):
            user_email = request.form.get('approve')
            if not user_email:
                return redirect(url_for('admin.startup_account'))
            approve_account(user_email, False)

        elif request.form.get('disapprove'):
            user_email = request.form.get('disapprove')
            if not user_email:
                return redirect(url_for('admin.startup_account'))
            disapprove_account(user_email, False)

        elif request.form.get("page"):
            page_no = request.form.get('page')
            return_data = all_str_data(page_no)
            return render_template('startup.html', inv_data=return_data)
        return redirect(url_for('admin.startup_account'))


@admin_blueprint.route('/get-single-startup', methods=["POST"])
@login_required
def get_startup_data():
    email = request.form.get('email')
    user_obj = Startup.objects.filter(email=email).first()
    if not user_obj:
        return jsonify({"result": False})

    ma_ser = StartupSerializeSingle()
    ser_data = ma_ser.dump(user_obj)
    ret_obj = jsonify({"result": True, "data": ser_data})
    ret_obj.headers.add('Access-Control-Allow-Origin', '*')
    return ret_obj


#<==================================================================================================>
#                                       DEALS PER WEEK
#<==================================================================================================>
@admin_blueprint.route('/deals-per-week', methods=["GET", "POST"])
@login_required
def deals_per_week():
    def helper_function(new_limit: int, collection: (Investor, Startup)):
        limit = 50
        total_inv_count = collection.objects.count()
        for offset in range(0, total_inv_count, limit):
            inv_data_chunk = collection.objects.skip(offset).limit(limit)
            for user in inv_data_chunk:
                setattr(user, "show_limit", new_limit)
                user.save()
                update_into_matching(user.email, new_limit, True)
        clean_discover()

    if request.method == "GET":
        return render_template("deals_per_week.html")

    elif request.method == "POST":
        if request.form.get("inv_deals"):
            new_limit = int(request.form.get("inv_deals"))
            helper_function(new_limit, Investor)
            flash(f"All investor's show limit updated to {new_limit}")
            return render_template("deals_per_week.html")

        elif request.form.get("str_deals"):
            new_limit = int(request.form.get("str_deals"))
            helper_function(new_limit, Startup)
            flash(f"All Startup's show limit updated to {new_limit}")
            return render_template("deals_per_week.html")


#<==================================================================================================>
#                                       INVESTORS DATA POPULATE
#<==================================================================================================>
@admin_blueprint.route('/inv-data-populate', methods=["GET", "POST"])
@login_required
def inv_data_populate():
    def get_data():
        data = {}
        inv_beta_data = InvestorBetaData.objects.all()
        ma_schema = InvestorBetaSchema()
        res = ma_schema.dump(inv_beta_data, many=True)
        if res:
            data["result"] = True
            data["data"] = res
        else:
            data["result"] = False
            data["data"] = []
        return data

    if request.method == "GET":
        return render_template("inv_beta_data.html", inv_beta=get_data())

    elif request.method == "POST":
        if request.files:
            file_obj = request.files.get('inv_csv')

            if not file_obj:
                flash("No file found. Please input a file")
                return render_template("inv_beta_data.html", inv_beta=get_data())

            else:
                res = file_process(file_obj, True, True)
                if res:
                    flash("All Investor's updated successfully")
                    return redirect(url_for('admin.inv_data_populate'))
                else:
                    flash("Some problem occurred while processing the file")
                    return redirect(url_for('admin.inv_data_populate'))
        else:
            action = request.form.get("action")
            if action == "delete_records":
                InvestorBetaData.objects.delete()
                flash("All beta links deleted")
                return render_template("inv_beta_data.html", inv_beta=get_data())


#<==================================================================================================>
#                                       INVESTORS BULK APPROVE
#<==================================================================================================>
@admin_blueprint.route('/investor-bulk-approve', methods=["POST"])
@login_required
def investor_bulk_approve():
    email_list = request.form.getlist('email_list[]')
    for email in email_list:
        approve_account(email, True)

    ret_obj = jsonify({"result": True, "data": "all accounts approved if they exists"})
    ret_obj.headers.add('Access-Control-Allow-Origin', '*')
    return ret_obj


#<==================================================================================================>
#                                       STARTUP BULK APPROVE
#<==================================================================================================>
@admin_blueprint.route('/startup-bulk-approve', methods=["POST"])
@login_required
def startup_bulk_approve():
    email_list = request.form.getlist('email_list[]')
    for email in email_list:
        approve_account(email, False)

    ret_obj = jsonify({"result": True, "data": "all accounts approved if they exists"})
    ret_obj.headers.add('Access-Control-Allow-Origin', '*')
    return ret_obj


#<==================================================================================================>
#                                         ANALYTICS
#<==================================================================================================>
@admin_blueprint.route('/analytics', methods=["GET"])
@login_required
def analytics():
    data = complete_analytics()
    return render_template("analytics.html", data=data)


#<==================================================================================================>
#                                         RETENTION
#<==================================================================================================>
@admin_blueprint.route('/retention', methods=["GET", "POST"])
@login_required
def retention():
    if request.method == "GET":
        inv_data = investor_retention(0)
        str_data = startup_retention(0)
        su_data = {"result": False, "data": None}
        return render_template("retention.html", inv_data=inv_data,
                               str_data=str_data, su_data=su_data)

    elif request.method == "POST":
        email = request.form.get("single_user_retention")
        is_inv = True if request.form.get("inlineRadioOptions") == "inv" else False

        su_data = user_retention(email, is_inv)
        if not su_data.get("result"):
            flash(su_data.get("error"))
            return redirect(url_for("admin.retention"))
        else:
            inv_data = investor_retention(0)
            str_data = startup_retention(0)
            return render_template("retention.html", inv_data=inv_data,
                                   str_data=str_data, su_data=su_data)