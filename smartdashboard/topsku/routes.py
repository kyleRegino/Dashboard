from flask import render_template, request, url_for, jsonify, Response, Blueprint
from smartdashboard import session, top_sku_talendfc
from smartdashboard.utils import init_list
from datetime import date
from sqlalchemy.sql import func

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
    total = []

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

    total_brands = session.query(func.sum(top_sku_talendfc.txn_amount)).scalar() 
    # total_brands = session.query(func.sum(top_sku_talendfc.txn_amount)).scalar().filter(and_(top_sku_talendfc.processing_dthr =="0500H", top_sku_talendfc.file_date == date.today())).scalar()
    print(total_brands)

    result_set = {
        "home": home,
        "smart_bro_prepaid": smart_bro_prepaid,
        "smart_prepaid": smart_prepaid,
        "sun_bwl_flp": sun_bwl_flp,
        "sun_bwl_prepaid": sun_bwl_prepaid,
    }

    return jsonify(result_set)

