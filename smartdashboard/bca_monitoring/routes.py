from flask import render_template, request, url_for, jsonify, Response, Blueprint
from smartdashboard.models import Job_BCA
from sqlalchemy import or_, and_
from smartdashboard import db, bca_monitoring_table, bca_dq_prp, bca_dq_pcodes
from datetime import date, datetime, timedelta
from smartdashboard.utils import time_to_seconds, init_list
from dateutil.relativedelta import relativedelta

bca_blueprint = Blueprint('bca_blueprint', __name__)

@bca_blueprint.route('/bca_monitoring', methods=['GET', 'POST'])
def bca_monitoring():
    page = request.args.get('page', 1, type=int)
    bca_query = Job_BCA.query.order_by(Job_BCA.RunDate.desc()).paginate(page=page, per_page=10)

    return render_template('bca_monitoring.html', bca_query = bca_query)

# @bca_blueprint.route('/bca_monitoring_search', methods=['GET', 'POST'])
# def bca_monitoring_search():
#     page = request.args.get('page', 1, type=int)

#     global search, tag
#     if request.method == 'POST' and 'tag' in request.form:
#         tag = request.form["tag"]
#         search = "%{}%".format(tag)

#     search_string = Job_BCA.query.filter(or_(Job_BCA.RunDate.like(search), 
#                                             Job_BCA.Dly_Prp_Acct.like(search), 
#                                             Job_BCA.Dly_PCODES.like(search), 
#                                             Job_BCA.UsageType_Total.like(search), 
#                                             Job_BCA.UsageType_DataDeducts.like(search),
#                                             Job_BCA.UsageType_SMSDeducts.like(search),
#                                             Job_BCA.UsageType_VoiceDeducts.like(search),
#                                             Job_BCA.UsageType_VasDeducts.like(search),
#                                             Job_BCA.UsageType_Topup.like(search), 
#                                             Job_BCA.UsageType_Expiration.like(search),
#                                                     ))\
#                                                         .order_by(Job_BCA.RunDate.desc()).paginate(page=page, per_page=10)
#     search_next_num = url_for('bca_blueprint.bca_monitoring_search', page=search_string.next_num) \
#         if search_string.has_next else None
#     search_prev_num = url_for('bca_blueprint.bca_monitoring_search', page=search_string.prev_num) \
#         if search_string.has_prev else None

#     return render_template('bca_monitoring_search.html', bca_query=search_string, 
#                                         tag=tag,
#                                         search=search,
#                                         next_num=search_next_num,
#                                         prev_num=search_prev_num
#                                         )   

@bca_blueprint.route('/bca_monitoring_date', methods=['GET', 'POST'])
def bca_monitoring_date():
    page = request.args.get('page', 1, type=int)

    global mindate, maxdate, minDate, maxDate
    if request.method == 'POST' and 'start_date' in request.form or 'end_date' in request.form:
        minDate = request.form["start_date"]
        maxDate = request.form["end_date"]
        mindate = "{}%".format(minDate)
        maxdate = "{}%".format(maxDate)

    search_string = Job_BCA.query.filter(and_(Job_BCA.RunDate >= mindate, Job_BCA.RunDate <= maxdate), 
                                            # Job_BCA.RunDate.like(maxdate), 
                                                    )\
                                                        .order_by(Job_BCA.RunDate.desc()).paginate(page=page, per_page=10)
    search_next_num = url_for('bca_blueprint.bca_monitoring_date', page=search_string.next_num) \
        if search_string.has_next else None
    search_prev_num = url_for('bca_blueprint.bca_monitoring_date', page=search_string.prev_num) \
        if search_string.has_prev else None

    return render_template('bca_monitoring_search.html', bca_query=search_string, 
                                        minDate=minDate,
                                        maxDate=maxDate,
                                        next_num=search_next_num,
                                        prev_num=search_prev_num)
                                        

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

@bca_blueprint.route('/bca_monitoring_dq', methods=['GET'])
def bca_monitoring_dq():
    return render_template('bca_dq.html')

@bca_blueprint.route('/bca_monitoring_dq_prp', methods=['GET', 'POST'])
def bca_monitoring_dq_prp():
    if request.method == "POST":
        start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()
    elif request.method == "GET":
        end_date = date.today()
        start_date = end_date - relativedelta(months=1)

    dates = [start_date + timedelta(days=x) for x in range(0, (end_date-start_date).days+1)]
    lookup = db.session.query(bca_dq_prp).filter(and_(bca_dq_prp.cre_dt >= start_date, bca_dq_prp.cre_dt <= end_date)).all()

    result_set = {
        "dates": [ d.strftime("%Y-%m-%d") for d in dates ],
        "data": {}
    }
    
    for l in lookup:
        if l.brand not in result_set["data"].keys():
            result_set["data"][l.brand] = {
                "bal": init_list(len(dates)),
                "count": init_list(len(dates)),
                "su": init_list(len(dates))
            }
            result_set["data"][l.brand]["bal"][dates.index(l.cre_dt)] = l.total_bal
            result_set["data"][l.brand]["count"][dates.index(l.cre_dt)] = l.total_count 
            result_set["data"][l.brand]["su"][dates.index(l.cre_dt)] = l.total_su
        else:
            result_set["data"][l.brand]["bal"][dates.index(l.cre_dt)] = l.total_bal
            result_set["data"][l.brand]["count"][dates.index(l.cre_dt)] = l.total_count 
            result_set["data"][l.brand]["su"][dates.index(l.cre_dt)] = l.total_su
    
    return jsonify(result_set)

@bca_blueprint.route('/bca_monitoring_dq_pcodes', methods=['GET', 'POST'])
def bca_monitoring_dq_pcodes():
    if request.method == "POST":
        start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()
    elif request.method == "GET":
        end_date = date.today()
        start_date = end_date - relativedelta(months=1)

    dates = [start_date + timedelta(days=x) for x in range(0, (end_date-start_date).days+1)]
    lookup = db.session.query(bca_dq_pcodes).filter(and_(bca_dq_pcodes.effective_date >= start_date, bca_dq_pcodes.effective_date <= end_date)).all()

    result_set = {
        "dates": [ d.strftime("%Y-%m-%d") for d in dates ],
        "data": {}
    }
    
    for l in lookup:
        if l.brand not in result_set["data"].keys():
            result_set["data"][l.brand] = {
                "total_topup": init_list(len(dates)),
                "topup_count": init_list(len(dates)),
                "total_count": init_list(len(dates))
            }
            result_set["data"][l.brand]["total_topup"][dates.index(l.effective_date)] = l.total_topup
            result_set["data"][l.brand]["topup_count"][dates.index(l.effective_date)] = l.count_topup 
            result_set["data"][l.brand]["total_count"][dates.index(l.effective_date)] = l.total_count
        else:
            result_set["data"][l.brand]["total_topup"][dates.index(l.effective_date)] = l.total_topup
            result_set["data"][l.brand]["topup_count"][dates.index(l.effective_date)] = l.count_topup 
            result_set["data"][l.brand]["total_count"][dates.index(l.effective_date)] = l.total_count
    
    return jsonify(result_set)


# FOR LZERO
@bca_blueprint.route('/bca_monitoring_lzero', methods=['GET', 'POST'])
def bca_monitoring_lzero():
    page = request.args.get('page', 1, type=int)
    bca_query = Job_BCA.query.order_by(Job_BCA.RunDate.desc()).paginate(page=page, per_page=10)

    return render_template('bca_monitoring_lzero.html', bca_query = bca_query)

@bca_blueprint.route('/bca_monitoring_date_lzero', methods=['GET', 'POST'])
def bca_monitoring_date_lzero():
    page = request.args.get('page', 1, type=int)

    global mindate, maxdate, minDate, maxDate
    if request.method == 'POST' and 'start_date' in request.form or 'end_date' in request.form:
        minDate = request.form["start_date"]
        maxDate = request.form["end_date"]
        mindate = "{}".format(minDate)
        maxdate = "{}".format(maxDate)

    # search_string = Job_BCA.query.filter(or_(Job_BCA.RunDate.like(mindate), 
    #                                         Job_BCA.RunDate.like(maxdate), 
    #                                                 ))\
    #                                                     .order_by(Job_BCA.RunDate.desc()).paginate(page=page, per_page=10)

    search_string = Job_BCA.query.filter(and_(Job_BCA.RunDate >= mindate, Job_BCA.RunDate <= maxdate), 
                                            # Job_BCA.RunDate.like(maxdate), 
                                                    )\
                                                        .order_by(Job_BCA.RunDate.desc()).paginate(page=page, per_page=10)
    search_next_num = url_for('bca_blueprint.bca_monitoring_date', page=search_string.next_num) \
        if search_string.has_next else None
    search_prev_num = url_for('bca_blueprint.bca_monitoring_date', page=search_string.prev_num) \
        if search_string.has_prev else None

    return render_template('bca_monitoring_search_lzero.html', bca_query=search_string, 
                                        minDate=minDate,
                                        maxDate=maxDate,
                                        next_num=search_next_num,
                                        prev_num=search_prev_num)