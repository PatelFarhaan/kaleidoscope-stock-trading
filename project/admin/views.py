from werkzeug.security import check_password_hash
from project.models import Investor, Startup, AdminPortal
from flask_login import login_required, login_user, logout_user
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from project.admin.admin_serializer import InvestorSerialize, StartupSerialize, StartupSerializeSingle, InvestorSerializeSingle


admin_blueprint = Blueprint('admin', '__name__', template_folder='templates', static_folder='static', url_prefix='/admin')


#<==================================================================================================>
#                                    ADMIN PANEL LOGIN
#<==================================================================================================>
@admin_blueprint.route('/login')
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    required = (email, password)
    if not all(required):
        return jsonify({"result": False, "message": "Email and Password are manditory fields"})

    admin_obj = AdminPortal.objects.filter(email=email).first()
    if not admin_obj:
        return jsonify({"result": False, "message": "user does not exist"})

    if check_password_hash(admin_obj.password, password):
        login_user(admin_obj)
        return redirect(url_for('admin.investor_account'))
    return jsonify({"result": False, "message": "Wrong Credentials"})



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
        if request.form.get('approve'):
            print(request.form)
            user_email = request.form.get('approve')
            if not user_email:
                return redirect(url_for('admin.investor_account'))

            user_obj = Investor.objects.filter(email=user_email).first()
            if not user_obj:
                return redirect(url_for('admin.investor_account'))

            user_obj.approved = True
            user_obj.save()

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