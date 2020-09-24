from flask import render_template, request, url_for, jsonify, Response, Blueprint
from smartdashboard import db, durations
from sqlalchemy import or_, and_
from sqlalchemy.sql import func
from smartdashboard.utils import format_date, init_list, number_formatter
from datetime import date, datetime, timedelta, time
from pprint import pprint
average_durations_blueprint = Blueprint('average_durations_blueprint', __name__)

@average_durations_blueprint.route('/sprint2', methods=['GET'])
def sprint2():
    return render_template('sprint2_duration.html')

@average_durations_blueprint.route('/sprint3', methods=['GET'])
def sprint3():
    return render_template('sprint2_duration.html')

@average_durations_blueprint.route('/sprint2_api', methods=['GET','POST'])
def sprint2_api():
    if request.method == "POST":
        ### EXECUTES AGGREGATE PER DAY OF DATE RANGE POSTED BY FORM
        start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()
        dates = [start_date + timedelta(days=x) for x in range(0, (end_date-start_date).days+1)]
        lookup = db.session.query(durations.file_date,durations.cdr_type,
                        func.avg(durations.average_duration),func.avg(durations.file_count))\
                        .filter(and_(durations.file_date >= start_date,
                        durations.file_date <= end_date,
                        durations.cdr_type.in_(("cbs_cdr_com","cbs_cdr_mon","cbs_cdr_cm","cbs_cdr_adj","cbs_cdr_first","cbs_cdr_vou"))))\
                        .group_by(durations.file_date,durations.cdr_type).all()
        
        result = {"dates":[ d.strftime("%Y-%m-%d") for d in dates ],"data":{}}

        for l in lookup:
            # if l.file_date not in result["dates"]:
            #     result["dates"][dates.index(l.file_date)] = l.file_date.strftime("%Y-%m-%d")
            if l.cdr_type not in result["data"].keys():
                result["data"][l.cdr_type] = {
                                                "duration": init_list(len(dates)),
                                                "count": init_list(len(dates)), 
                                            }
                result["data"][l.cdr_type]["duration"][dates.index(l.file_date)] = str(l[2])
                result["data"][l.cdr_type]["count"][dates.index(l.file_date)] = str(l[3])
            else:
                result["data"][l.cdr_type]["duration"][dates.index(l.file_date)] = str(l[2])
                result["data"][l.cdr_type]["count"][dates.index(l.file_date)] = str(l[3])

    else:
        # EXECUTES 24 HOUR FORMAT
        dt_now = datetime.now()
        if dt_now.hour == 0:
            yesterday = date.today() - timedelta(days=1)
            lookup = db.session.query(durations.file_date,durations.cdr_type,
                        durations.hour,
                        durations.average_duration,durations.file_count)\
                        .filter(and_(durations.file_date == yesterday,
                        durations.cdr_type.in_(("cbs_cdr_com","cbs_cdr_mon","cbs_cdr_cm","cbs_cdr_adj","cbs_cdr_first","cbs_cdr_vou"))))\
                        .all()
            
            start_dt = datetime.combine(yesterday,time(0,0))
            dates = [start_dt + timedelta(hours=x) for x in range(24)]

        else:
            start_hour = datetime.now().hour
            end_hour = datetime.now().hour - 1
            start_date = (dt_now - timedelta(hours=24)).date()
            end_date = dt_now.date()
            lookup = db.session.query(durations.file_date,durations.cdr_type,
                        durations.hour,
                        durations.average_duration,durations.file_count)\
                        .filter(durations.cdr_type.in_(("cbs_cdr_com","cbs_cdr_mon","cbs_cdr_cm","cbs_cdr_adj","cbs_cdr_first","cbs_cdr_vou")))\
                        .filter(or_(and_(durations.file_date == start_date,durations.hour >= start_hour),and_(durations.file_date == end_date,durations.hour <= end_hour))).all()
            
            start_dt = datetime.combine(start_date,time(start_hour,0))
            dates = [start_dt + timedelta(hours=x) for x in range(24)]

        result = {"dates":[ d.strftime("%Y-%m-%d %I %p") for d in dates ],"data":{}}

        for l in lookup:
            dt = datetime.combine(l.file_date,time(l.hour,0))
            # if dt not in result["dates"]:
            #     result["dates"][dates.index(l.file_date)] = l.file_date.strftime("%Y-%m-%d")
            if l.cdr_type not in result["data"].keys():
                result["data"][l.cdr_type] = {
                                                "duration": init_list(len(dates)),
                                                "count": init_list(len(dates)), 
                                            }
                
                result["data"][l.cdr_type]["duration"][dates.index(dt)] = str(l[3])
                result["data"][l.cdr_type]["count"][dates.index(dt)] = str(l[4])
            else:
                result["data"][l.cdr_type]["duration"][dates.index(dt)] = str(l[3])
                result["data"][l.cdr_type]["count"][dates.index(dt)] = str(l[4])

    

    return jsonify(result)

@average_durations_blueprint.route('/sprint3_api', methods=['GET','POST'])
def sprint3_api():
    if request.method == "POST":
        start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()
    else:
        today = date.today()
        start_date = today - relativedelta(months=1)
        end_date = today

    dates = [start_date + timedelta(days=x) for x in range(0, (end_date-start_date).days+1)]
    lookup = db.session.query(durations).filter(and_(durations.file_date >= start_date,durations.file_date <= end_date,durations.cdr_type.in_(("cbs_cdr_data","cbs_cdr_voice","cbs_cdr_sms","cbs_cdr_clr")))).all()

    result = {"dates":[ d.strftime("%Y-%m-%d") for d in dates ],"data":{}}

    for l in lookup:
        if l.file_date not in result["dates"]:
            result["dates"][dates.index(l.file_date)] = l.file_date.strftime("%Y-%m-%d")
        if l.cdr_type not in result["data"].keys():
            result["data"][l.cdr_type] = {
                                            "duration": init_list(len(dates)),
                                            "count": init_list(len(dates)), 
                                        }
            pprint(result)
            result["data"][l.cdr_type]["duration"][dates.index(l.file_date)] = number_formatter(l.average_duration)
            result["data"][l.cdr_type]["count"][dates.index(l.file_date)] = number_formatter(l.file_count)
        else:
            result["data"][l.cdr_type]["duration"][dates.index(l.file_date)] = number_formatter(l.average_duration)
            result["data"][l.cdr_type]["count"][dates.index(l.file_date)] = number_formatter(l.file_count)

    return jsonify(result)

