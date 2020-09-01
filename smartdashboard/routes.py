from flask import render_template, request, url_for, jsonify

from smartdashboard import app,  session, bca_monitoring_table, manifest_hive_monitoring, manifest_oracle_monitoring
from smartdashboard.models import Job_Monitoring, Job_BCA, Dly_Usagetype, Dly_Prp_Acct, Dly_Pcodes, topsku_prod, topsku_talend
from smartdashboard.utils import time_to_seconds, init_list

from sqlalchemy import or_, and_
from sqlalchemy.sql import func
from flask import jsonify, Response

from datetime import datetime
from datetime import date

import io, csv

from openpyxl import Workbook



# TOPSKU
@app.route('/topksu_talend', methods=['GET', 'POST'])
def topksu_talend():
    query_prod = topsku_prod.query.all()
    query_talend = topsku_talend.query.all()

    for prod in query_prod:
        # if prod.processing_dttm >= 'currentdatetime' OR prod.processing_dttm <= 
        if datetime.strptime("13:00:00", "%H:%M:%S") in prod.processing_dttm:
            print(prod)

    print(query_prod)   

    return render_template('topsku_talend.html', query_prod = query_prod, query_talend = query_talend)
