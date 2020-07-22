import threading
from werkzeug.security import check_password_hash
from project.models import Investor, Startup, AdminPortal
from common_utilities.file_processing import inv_file_process
from flask_login import login_required, login_user, logout_user
from common_utilities.wait_list_completed_startup import wait_list_over_str
from common_utilities.wait_list_completed_investor import wait_list_over_inv
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
from project.admin.admin_serializer import InvestorSerialize, StartupSerialize, StartupSerializeSingle,\
                                           InvestorSerializeSingle


admin_blueprint = Blueprint('admin', '__name__', template_folder='templates', static_folder='static', url_prefix='/admin')


#<==================================================================================================>
#                                    ADMIN PANEL LOGIN
#<==================================================================================================>
@admin_blueprint.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        required = (email, password)
        if not all(required):
            return render_template('login.html', res={"result": False, "message": "Email and Password are Manditory"})

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
    return jsonify({"result": True, "message": "user logged out successfully"})


#<==================================================================================================>
#                          INVESTOR ACCOUNT + PAGINATION + SINGLE USER
#<==================================================================================================>
@admin_blueprint.route('/investor-account', methods=["GET", "POST"])
@login_required
def investor_account():
    if request.method == "GET":
        resp = Investor.objects.limit(10)
        ma_ser = InvestorSerialize()
        if resp != []:
            total_inv_counts = Investor.objects.count()
            res = ma_ser.dump(resp, many=True)
            return_data = {}
            return_data["result"] = True
            return_data["data"] = res
            total_str_counts = Startup.objects.count()
            return_data["total_count_str"] = total_str_counts
            return_data["total_count_inv"] = total_inv_counts
        else:
            return_data = {}
            return_data["result"] = False
            return_data["data"] = None
            total_str_counts = Startup.objects.count()
            return_data["total_count_str"] = total_str_counts
            return_data["total_count_inv"] = 0
        return render_template('investor.html', inv_data=return_data)

    elif request.method == "POST":
        if request.files:
            file_obj = request.files.get('inv_csv')

            if not file_obj:
                return redirect(url_for('admin.investor_account'))

            res = inv_file_process(file_obj, True)
            if res:
                session["success"] = "All Investor's updated successfully"
                return redirect(url_for('admin.investor_account'))
            else:
                session["errors"] = "Some problem occurred while processing the file"
                return redirect(url_for('admin.investor_account'))

        elif request.form.get('approve'):
            user_email = request.form.get('approve')
            if not user_email:
                return redirect(url_for('admin.investor_account'))

            user_obj = Investor.objects.filter(email=user_email).first()
            if not user_obj:
                return redirect(url_for('admin.investor_account'))

            user_obj.approved = True
            user_obj.save()

            email, first_name = user_obj.email, user_obj.first_name
            thread = threading.Thread(target=wait_list_over_inv, args=(email, first_name,))
            thread.start()

        elif request.form.get('disapprove'):
            user_email = request.form.get('disapprove')
            if not user_email:
                return redirect(url_for('admin.investor_account'))

            user_obj = Investor.objects.filter(email=user_email).first()
            if not user_obj:
                return redirect(url_for('admin.investor_account'))

            user_obj.approved = False
            user_obj.save()

        elif request.form.get("page"):
            page_no = request.form.get('page')
            offset = 10 * int(page_no)
            resp = Investor.objects.skip(int(offset)).limit(10)
            if resp != []:
                total_inv_counts = Investor.objects.count()
                total_str_counts = Startup.objects.count()
                ma_ser = InvestorSerialize()
                res = ma_ser.dump(resp, many=True)
                return_data = {}
                return_data["result"] = True
                return_data["data"] = res
                return_data["total_count_inv"] = total_inv_counts
                return_data["total_count_str"] = total_str_counts
            else:
                return_data = {}
                return_data["result"] = False
                return_data["data"] = None
                return_data["total_count_inv"] = 0
                total_str_counts = Startup.objects.count()
                return_data["total_count_str"] = total_str_counts
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
    if request.method == "GET":
        resp = Startup.objects.limit(10)
        ma_ser = StartupSerialize()
        if resp != []:
            total_str_counts = Startup.objects.count()
            res = ma_ser.dump(resp, many=True)
            return_data = {}
            return_data["result"] = True
            return_data["data"] = res
            total_inv_counts = Investor.objects.count()
            return_data["total_count_str"] = total_str_counts
            return_data["total_count_inv"] = total_inv_counts
        else:
            return_data = {}
            return_data["result"] = False
            return_data["data"] = None
            total_inv_counts = Investor.objects.count()
            return_data["total_count_str"] = 0
            return_data["total_count_inv"] = total_inv_counts
        return render_template('startup.html', inv_data=return_data)

    elif request.method == "POST":
        if request.files:
            file_obj = request.files.get('str_csv')

            if not file_obj:
                return redirect(url_for('admin.startup_account'))

            res = inv_file_process(file_obj, False)
            if res:
                session["success"] = "All Startup's updated successfully"
                return redirect(url_for('admin.startup_account'))
            else:
                session["errors"] = "Some problem occurred while processing the file"
                return redirect(url_for('admin.startup_account'))

        if request.form.get('approve'):
            print(request.form)
            user_email = request.form.get('approve')
            if not user_email:
                return redirect(url_for('admin.investor_account'))

            user_obj = Startup.objects.filter(email=user_email).first()
            if not user_obj:
                return redirect(url_for('admin.startup_account'))

            user_obj.approved = True
            user_obj.save()

            email, first_name = user_obj.email, user_obj.first_name
            thread = threading.Thread(target=wait_list_over_str, args=(email, first_name,))
            thread.start()

        elif request.form.get('disapprove'):
            user_email = request.form.get('disapprove')
            if not user_email:
                return redirect(url_for('admin.investor_account'))

            user_obj = Startup.objects.filter(email=user_email).first()
            if not user_obj:
                return redirect(url_for('admin.startup_account'))

            user_obj.approved = False
            user_obj.save()

        elif request.form.get("page"):
            page_no = request.form.get('page')
            offset = 10 * int(page_no)
            resp = Startup.objects.skip(int(offset)).limit(10)
            if resp != []:
                total_inv_counts = Investor.objects.count()
                total_str_counts = Startup.objects.count()
                ma_ser = StartupSerialize()
                res = ma_ser.dump(resp, many=True)
                return_data = {}
                return_data["result"] = True
                return_data["data"] = res
                return_data["total_count_inv"] = total_inv_counts
                return_data["total_count_str"] = total_str_counts
            else:
                return_data = {}
                return_data["result"] = False
                return_data["data"] = None
                return_data["total_count_str"] = 0
                total_inv_counts = Investor.objects.count()
                return_data["total_count_inv"] = total_inv_counts
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
    if request.method == "GET":
        return render_template("deals_per_week.html")
    elif request.method == "POST":
        if request.form.get("inv_deals"):
            limit = 50
            new_limit = int(request.form.get("inv_deals"))
            total_inv_count = Investor.objects.count()
            for offset in range(0, total_inv_count, limit):
                inv_data_chunk = Investor.objects.skip(offset).limit(limit)
                for inv in inv_data_chunk:
                    setattr(inv, "show_limit", new_limit)
                    inv.save()
            flash(f"All investor's show limit updated to {new_limit}")
            return render_template("deals_per_week.html")

        elif request.form.get("str_deals"):
            limit = 50
            new_limit = int(request.form.get("str_deals"))
            total_str_count = Startup.objects.count()
            for offset in range(0, total_str_count, limit):
                str_data_chunk = Startup.objects.skip(offset).limit(limit)
                for str in str_data_chunk:
                    setattr(str, "show_limit", new_limit)
                    str.save()
            flash(f"All Startup's show limit updated to {new_limit}")
            return render_template("deals_per_week.html")


#<==================================================================================================>
#                                       INVESTORS DATA POPULATE
#<==================================================================================================>
@admin_blueprint.route('/inv-data-populate', methods=["GET", "POST"])
@login_required
def inv_data_populate():
    if request.method == "GET":
        return render_template("inv_beta_data.html")

    elif request.method == "POST":
        if request.files:
            file_obj = request.files.get('inv_csv')

            if not file_obj:
                flash("No file found. Please input a file")
                return render_template("inv_beta_data.html")

            else:
                res = inv_file_process(file_obj, True)
                if res:
                    flash("All Investor's updated successfully", category="message")
                    return redirect(url_for('admin.investor_account'))
                else:
                    flash("Some problem occurred while processing the file")
                    return redirect(url_for('admin.investor_account'))


#<==================================================================================================>
#                                       STARTUP DATA POPULATE
#<==================================================================================================>
@admin_blueprint.route('/srt-data-populate', methods=["GET", "POST"])
@login_required
def str_data_populate():
    if request.method == "GET":
        return render_template("str_beta_data.html")

    elif request.method == "POST":
        if request.files:
            file_obj = request.files.get('str_csv')

            if not file_obj:
                flash("No file found. Please input a file")
                return render_template("str_beta_data.html")

            else:
                flash("File found.")
                return render_template("str_beta_data.html")

            # res = inv_file_process(file_obj, True)
            # if res:
            #     flash("All Investor's updated successfully", category="message")
            #     return redirect(url_for('admin.investor_account'))
            # else:
            #     flash("Some problem occurred while processing the file")
            #     return redirect(url_for('admin.investor_account'))