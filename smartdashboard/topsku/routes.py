from flask import render_template, request, url_for, jsonify, Response, Blueprint
from smartdashboard import session, top_sku_talendfc
from datetime import date, datetime, timedelta
from sqlalchemy.sql import func
from sqlalchemy import or_, and_
from smartdashboard.utils import format_date, init_list, insert_sku
import pprint

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

    lookup = session.query(top_sku_talendfc.txn_date,top_sku_talendfc.processing_dthr,top_sku_talendfc.brand, func.sum(top_sku_talendfc.txn_amount), func.sum(top_sku_talendfc.topup_cnt)).filter(top_sku_talendfc.txn_date == query_date).group_by(top_sku_talendfc.txn_date,top_sku_talendfc.processing_dthr,top_sku_talendfc.brand).all()
    
    sku_dict = { "totals": {
                    "total_amt_hr": init_list(6,0),
                    "total_cnt_hr": init_list(6,0)
                    },
                 "brands": { }
        }
    for l in lookup:
        if l.brand not in sku_dict["brands"].keys():
            sku_dict["brands"][l.brand] = {
                "amount": init_list(6,0),
                "count": init_list(6,0)
            }
            insert_sku(sku_dict["brands"][l.brand], l.processing_dthr, l[3], l[4])
        else:
            insert_sku(sku_dict["brands"][l.brand], l.processing_dthr, l[3], l[4])

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
    lookup = session.query(top_sku_talendfc.txn_date,func.sum(top_sku_talendfc.txn_amount),func.sum(top_sku_talendfc.topup_cnt)).filter(and_(top_sku_talendfc.txn_date >= start_date, top_sku_talendfc.txn_date <= end_date)).group_by(top_sku_talendfc.txn_date).all()

    sku_dict = { "dates": [ d.strftime("%Y-%m-%d") for d in dates ],
                 "amounts": init_list(len(dates)),
                 "counts": init_list(len(dates))
            }
   
    for l in lookup:
        print(dates.index(l.txn_date))
        try:
            sku_dict["amounts"][dates.index(l.txn_date)] = str(l[1])
            sku_dict["counts"][dates.index(l.txn_date)] = str(l[2])
        except:
            continue

   
    return jsonify(sku_dict)