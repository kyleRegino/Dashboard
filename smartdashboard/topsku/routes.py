from flask import render_template, request, url_for, jsonify, Response, Blueprint
from smartdashboard import session, top_sku_talendfc
from datetime import date
from sqlalchemy.sql import func
from sqlalchemy import or_, and_
from smartdashboard.utils import format_date, init_list

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

    dates = session.query(top_sku_talendfc.processing_dthr).filter(top_sku_talendfc.txn_date == query_date).group_by(top_sku_talendfc.processing_dthr).all()
    amounts = session.query(top_sku_talendfc.processing_dthr, top_sku_talendfc.brand, top_sku_talendfc.txn_amount).filter(top_sku_talendfc.txn_date == query_date).all()
    len_date = len(dates)
    
    date_list = init_list(len_date)
    home = init_list(len_date)
    smart_bro_prepaid = init_list(len_date)
    smart_prepaid = init_list(len_date)
    sun_bwl_flp = init_list(len_date)
    sun_bwl_prepaid = init_list(len_date)
    sun_flp = init_list(len_date)
    sun_prepaid = init_list(len_date)
    tnt = init_list(len_date)
    
    total_hour = []
    total_day = []

    for i, d in enumerate(dates):
        for v in amounts:
            if v.brand == "HOME" and v[0] == d[0]:
                home[i] = str(v[2])
            elif v.brand == "SMART BRO PREPAID" and v[0] == d[0]:
                smart_bro_prepaid[i] = str(v[2])
            elif v.brand == "SMART PREPAID" and v[0] == d[0]:
                smart_prepaid[i] = str(v[2])
            elif v.brand == "SUN BW FLP" and v[0] == d[0]:
                sun_bwl_flp[i] = str(v[2])
            elif v.brand == "SUN BW PREPAID" and v[0] == d[0]:
                sun_bwl_prepaid[i] = str(v[2])
            elif v.brand == "SUN FLP" and v[0] == d[0]:
                sun_flp[i] = str(v[2])
            elif v.brand == "SUN PREPAID" and v[0] == d[0]:
                sun_prepaid[i] = str(v[2])
            elif v.brand == "TNT" and v[0] == d[0]:
                tnt[i] = str(v[2])

    #per hour run
    total_hour_query = session.query(top_sku_talendfc).filter(top_sku_talendfc.txn_date == query_date).with_entities(top_sku_talendfc.processing_dthr).distinct()
    for hour in total_hour_query:
        hours = session.query(func.sum(top_sku_talendfc.txn_amount)).filter(top_sku_talendfc.processing_dthr == hour).scalar()
        total_hour.append(hours)

    #per day run
    total_day_query = session.query(top_sku_talendfc).with_entities(top_sku_talendfc.txn_date).distinct()
    for day in total_day_query:
        days = session.query(func.sum(top_sku_talendfc.txn_amount)).filter(top_sku_talendfc.txn_date == day).scalar()
        total_day.append(days)
    # print(total_day)

    result_set = {
        "home": home,
        "smart bro prepaid": smart_bro_prepaid,
        "smart prepaid": smart_prepaid,
        "sun bw flp": sun_bwl_flp,
        "sun bw prepaid": sun_bwl_prepaid,
        "sun flp": sun_flp,
        "sun prepaid": sun_prepaid,
        "tnt": tnt,
        "total_hour": total_hour,
        "total_day": total_day
    }

    return jsonify(result_set)

