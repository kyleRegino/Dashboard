from flask import render_template, request, url_for, jsonify, Response, Blueprint
from smartdashboard import session, top_sku_talendfc
from smartdashboard.utils import init_list
from datetime import date
from sqlalchemy.sql import func
from sqlalchemy import or_, and_

topsku_blueprint = Blueprint('topsku_blueprint', __name__)

@topsku_blueprint.route('/topsku', methods=['GET', 'POST'])
def topsku():
    return render_template('topsku_talend.html')

@topsku_blueprint.route('/topsku_js', methods=['GET','POST'])
def topsku_js():
    if request.method == "POST":
        query_date = request.form["cdr_date"]
    else:
        query_date = date.today()

    results = session.query(top_sku_talendfc).all()
    home = []
    smart_bro_prepaid = []
    smart_prepaid = []
    sun_bwl_flp = []
    sun_bwl_prepaid = []
    total_hour = []
    total_day = []

    for r in results:
        if r.brand == "HOME":
            home.append(str(r.txn_amount))
        elif r.brand == "SMART BRO PREPAID":
            smart_bro_prepaid.append(str(r.txn_amount))
        elif r.brand == "SMART PREPAID":
            smart_prepaid.append(str(r.txn_amount))
        elif r.brand == "SUN BW FLP":
            sun_bwl_flp.append(str(r.txn_amount))
        elif r.brand == "SUN BW PREPAID":
            sun_bwl_prepaid.append(str(r.txn_amount))

    #per hour run
    total_hour_query = session.query(top_sku_talendfc).with_entities(top_sku_talendfc.processing_dthr).distinct()
    for hour in total_hour_query:
        hours = session.query(func.sum(top_sku_talendfc.txn_amount)).filter(top_sku_talendfc.processing_dthr == hour).scalar()
        total_hour.append(hours)

    print(total_hour)

    #per day run
    total_day_query = session.query(top_sku_talendfc).with_entities(top_sku_talendfc.txn_date).distinct()
    for day in total_day_query:
        days = session.query(func.sum(top_sku_talendfc.txn_amount)).filter(top_sku_talendfc.txn_date == day).scalar()
        total_day.append(days)
    print(total_day)

    result_set = {
        "home": home,
        "smart bro prepaid": smart_bro_prepaid,
        "smart prepaid": smart_prepaid,
        "sun bwl flp": sun_bwl_flp,
        "sun bwl prepaid": sun_bwl_prepaid,
        "total_hour": total_hour,
        "total_day": total_day
    }

    return jsonify(result_set)

