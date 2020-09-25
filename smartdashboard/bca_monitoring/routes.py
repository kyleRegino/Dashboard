from flask import render_template, request, url_for, jsonify, Response, Blueprint
from smartdashboard.models import Job_BCA
from sqlalchemy import and_
from smartdashboard import db, bca_monitoring_table
from datetime import date, datetime
from smartdashboard.utils import time_to_seconds
from dateutil.relativedelta import relativedelta

bca_blueprint = Blueprint('bca_blueprint', __name__)

@bca_blueprint.route('/bca_monitoring', methods=['GET', 'POST'])
def bca_monitoring():
    page = request.args.get('page', 1, type=int)
    bca_query = Job_BCA.query.order_by(Job_BCA.RunDate.desc()).paginate(page=page, per_page=50)

    return render_template('bca_monitoring.html', bca_query = bca_query)

@bca_blueprint.route('/get_bca_monitoring', methods=['GET','POST'])
def get_bca_monitoring():
    if request.method == "POST":
        start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()
    elif request.method == "GET":
        end_date = date.today()
        start_date = end_date - relativedelta(months=4)

    results = db.session.query(bca_monitoring_table).filter(and_(bca_monitoring_table.RunDate >= start_date,bca_monitoring_table.RunDate <= end_date )).all()
    dates = []
    usagetype_total = []
    prp_acct = []
    pcodes = []
    data = []
    expiration = []
    topup = []
    voice = []
    vas = []
    sms = []
    for r in results:
        dates.append(r.RunDate.strftime("%Y-%m-%d"))
        usagetype_total.append(time_to_seconds(r.UsageType_Total))
        prp_acct.append(time_to_seconds(r.Dly_Prp_Acct))
        pcodes.append(time_to_seconds(r.Dly_PCODES))
        data.append(time_to_seconds(r.UsageType_DataDeducts))
        expiration.append(time_to_seconds(r.UsageType_Expiration))
        topup.append(time_to_seconds(r.UsageType_Topup))
        voice.append(time_to_seconds(r.UsageType_VoiceDeducts))
        vas.append(time_to_seconds(r.UsageType_VasDeducts))
        sms.append(time_to_seconds(r.UsageType_SMSDeducts))


    result_set = {
        "dates": dates,
        "usagetype_total": usagetype_total,
        "prp_acct": prp_acct,
        "pcodes": pcodes,
        "data_deducts": data,
        "expiration": expiration,
        "topup_deducts": topup,
        "voice_deducts": voice,
        "vas_deducts": vas,
        "sms_deducts": sms
    }

    return jsonify(result_set)


# FOR LZERO
@bca_blueprint.route('/bca_monitoring_lzero', methods=['GET', 'POST'])
def bca_monitoring_lzero():
    page = request.args.get('page', 1, type=int)
    bca_query = Job_BCA.query.order_by(Job_BCA.RunDate.desc()).paginate(page=page, per_page=50)

    return render_template('bca_monitoring_lzero.html', bca_query = bca_query)