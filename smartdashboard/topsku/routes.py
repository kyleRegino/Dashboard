from flask import render_template, request, url_for, jsonify, Response, Blueprint
from smartdashboard import db, top_sku_talendfc
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy.sql import func
from sqlalchemy import or_, and_
from smartdashboard.utils import format_date, init_list, insert_sku, insert_sku_table, aggregate_sku_table
import pprint
from collections import OrderedDict
topsku_blueprint = Blueprint('topsku_blueprint', __name__)

@topsku_blueprint.route('/topsku', methods=['GET', 'POST'])
def topsku():
    return render_template('topsku_talend.html')

@topsku_blueprint.route('/topsku_day_js', methods=['GET','POST'])
def topsku_day_js():
    if request.method == "POST":
        query_date = request.form["sku_date"]
    else:
        query_date = date.today()

    lookup = db.session.query(top_sku_talendfc.txn_date,top_sku_talendfc.processing_hr,top_sku_talendfc.brand, func.sum(top_sku_talendfc.txn_amount), func.sum(top_sku_talendfc.topup_cnt)).filter(top_sku_talendfc.txn_date == query_date).group_by(top_sku_talendfc.txn_date,top_sku_talendfc.processing_hr,top_sku_talendfc.brand).all()
    
    sku_dict = { "totals": {
                    "total_amt_hr": init_list(6,0),
                    "total_cnt_hr": init_list(6,0)
                    },
                 "brands": OrderedDict({ })
        }
    for l in lookup:
        if l.brand not in sku_dict["brands"].keys():
            sku_dict["brands"][l.brand] = {
                "amount": init_list(6,0),
                "count": init_list(6,0)
            }
            insert_sku(sku_dict["brands"][l.brand], l.processing_hr, l[3], l[4])
        else:
            insert_sku(sku_dict["brands"][l.brand], l.processing_hr, l[3], l[4])

    for k in sku_dict["brands"].keys():
        for i in range(6):
            sku_dict["totals"]["total_amt_hr"][i] += float(0 if sku_dict["brands"][k]["amount"][i] is None else sku_dict["brands"][k]["amount"][i])
            sku_dict["totals"]["total_cnt_hr"][i] += int(0 if sku_dict["brands"][k]["count"][i] is None else sku_dict["brands"][k]["count"][i])
    
    return jsonify(sku_dict)

@topsku_blueprint.route('/topsku_week_js', methods=['GET','POST'])
def topsku_week_js():
    if request.method == "POST":
        start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()
    else:
        today = date.today()
        start_date = today - timedelta(days=today.weekday()+1)
        end_date = start_date + timedelta(days=6)

    dates = [start_date + timedelta(days=x) for x in range(0, (end_date-start_date).days+1)]
    lookup = db.session.query(top_sku_talendfc.txn_date,func.sum(top_sku_talendfc.txn_amount),func.sum(top_sku_talendfc.topup_cnt)).filter(and_(top_sku_talendfc.txn_date >= start_date, top_sku_talendfc.txn_date <= end_date, top_sku_talendfc.processing_hr == 1)).group_by(top_sku_talendfc.txn_date).all()

    sku_dict = { "dates": [ d.strftime("%Y-%m-%d") for d in dates ],
                 "amounts": init_list(len(dates)),
                 "counts": init_list(len(dates))
            }
   
    for l in lookup:
        try:
            sku_dict["amounts"][dates.index(l.txn_date)] = str(l[1])
            sku_dict["counts"][dates.index(l.txn_date)] = str(l[2])
        except:
            continue

   
    return jsonify(sku_dict)

@topsku_blueprint.route('/topsku_week_table_js', methods=['POST'])
def topsku_week_table_js():
    date = datetime.strptime(request.form["sku_date"],"%Y-%m-%d").date()
    hour = int(request.form["hour"])

    weekday = date.weekday()
    start_date = date - relativedelta(weeks=4, weekday=weekday)
    end_date = date
   
    # if start_date == "" and end_date == "" and date.today().weekday() != 6:
    #     date_today = date.today()
    #     start_date = date_today - relativedelta(weeks=4, weekday=MO(-1))
    #     end_date = start_date + relativedelta(weeks=3, weekday=SU(1))
    # elif start_date == "" and end_date == "" and date.today().weekday() == 6:
    #     date_today = date.today()
    #     start_date = date_today - relativedelta(weeks=4, weekday=MO(-1))
    #     end_date = date_today
    # else:
    #     start_date = datetime.strptime(start_date,"%Y-%m-%d").date() + relativedelta(weekday=MO(-1))
    #     end_date = datetime.strptime(end_date,"%Y-%m-%d").date() + relativedelta(weekday=SU(1))


    brands = db.session.query(func.distinct(top_sku_talendfc.brand)).filter(and_(top_sku_talendfc.txn_date >= start_date, top_sku_talendfc.txn_date <= end_date, func.weekday(top_sku_talendfc.txn_date) == weekday, top_sku_talendfc.processing_hr == hour))
    lookup = db.session.query(top_sku_talendfc.txn_date,top_sku_talendfc.brand,func.sum(top_sku_talendfc.txn_amount)).filter(and_(top_sku_talendfc.txn_date >= start_date, top_sku_talendfc.txn_date <= end_date, func.weekday(top_sku_talendfc.txn_date) == weekday, top_sku_talendfc.processing_hr == hour)).group_by(top_sku_talendfc.txn_date,top_sku_talendfc.brand)

    brands = [ b[0] for b in brands ] + ["TOTAL"]
    sku_dict = {}

    for l in lookup.all():
        key = l[0].strftime("%Y-%m-%d")
        if key not in sku_dict.keys():
            sku_dict[key] = {
                "brands": dict.fromkeys(brands,None),
            }
            sku_dict[key]["brands"][l[1]] = str(l[2])
            if sku_dict[key]["brands"]["TOTAL"] == None:
                sku_dict[key]["brands"]["TOTAL"] = 0
            sku_dict[key]["brands"]["TOTAL"] += l[2]
        else:
            if sku_dict[key]["brands"]["TOTAL"] == None:
                sku_dict[key]["brands"]["TOTAL"] = 0
            sku_dict[key]["brands"][l[1]] = str(l[2])
            sku_dict[key]["brands"]["TOTAL"] += l[2]
    # for l in lookup.all():
    #     cur_week = ""
    #     if l[1] not in sku_dict.keys():
    #         sku_dict[l[1]] = {
    #             "start_date": None,
    #             "end_date": None,
    #             "brands": dict.fromkeys(brands,None),
    #         }
            
    #         insert_sku_table(l,sku_dict[l[1]])
    #         aggregate_sku_table(l,sku_dict[l[1]])
    #     else:
    #         insert_sku_table(l,sku_dict[l[1]])
    #         aggregate_sku_table(l,sku_dict[l[1]])
   
    formatted_data = {
                    "columns": ["Dates"] + brands,
                    "data": []
                }
    for k in sku_dict.keys():
        sku = dict.fromkeys(formatted_data["columns"])
        sku["Dates"] = k
        for b in sku_dict[k]["brands"].keys():
            sku[b] = str(sku_dict[k]["brands"][b])
        formatted_data["data"].append(sku)
    # for k in sku_dict.keys():
    #     sku = dict.fromkeys(formatted_data["columns"])
    #     sku["Dates"] = str(sku_dict[k]["start_date"]) + " to " + str(sku_dict[k]["end_date"])
    #     for b in sku_dict[k]["brands"].keys():
    #         sku[b] = str(sku_dict[k]["brands"][b])
    #     formatted_data["data"].append(sku)
    
    return jsonify(formatted_data)
