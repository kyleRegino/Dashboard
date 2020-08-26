from flask import render_template, request, url_for, jsonify

from smartdashboard import app,  session, bca_monitoring_table, manifest_hive_monitoring, manifest_oracle_monitoring
from smartdashboard.models import Job_Monitoring, Job_BCA, Dly_Usagetype, Dly_Prp_Acct, Dly_Pcodes, topsku_prod, topsku_talend
from smartdashboard.forms import Search
from smartdashboard.utils import time_to_seconds

from sqlalchemy import or_, and_
from sqlalchemy.sql import func
from flask import jsonify, Response

from datetime import datetime

import io, csv

from openpyxl import Workbook

# DASHBOARD TAB
@app.route('/')
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    page = request.args.get('page', 1, type=int)
    query_string = Job_Monitoring.query.order_by(Job_Monitoring.starttime.desc()).paginate(page=page, per_page=50)
    query_job_running = Job_Monitoring.query.filter(Job_Monitoring.status == 'RUNNING').count()
    query_job_ok = Job_Monitoring.query.filter(Job_Monitoring.status == 'OK').count()
    query_job_error = Job_Monitoring.query.filter(Job_Monitoring.status == 'ERROR').count()
    query_job_misfired = Job_Monitoring.query.filter(Job_Monitoring.status == 'MISFIRED').count()

    query_distinct = Job_Monitoring.query.with_entities(Job_Monitoring.tasklabel).distinct()
    query_distinct_count = Job_Monitoring.query.with_entities(Job_Monitoring.tasklabel).distinct().count()
    long_running_count = Job_Monitoring.query.filter(Job_Monitoring.duration_mins >= 30).count()

    next_num = url_for('dashboard', page=query_string.next_num) \
            if query_string.has_next else None
    prev_num = url_for('dashboard', page=query_string.prev_num) \
        if query_string.has_prev else None

    if request.method == 'POST' and 'datetimepickermin' in request.form or 'datetimepickermax' in request.form:
        minDate = request.form["datetimepickermin"]
        maxDate = request.form["datetimepickermax"]
        min = "{}%".format(minDate)
        max = "{}%".format(maxDate)
        print(min)
        print(max)

    return render_template("dashboard.html", query = query_string,
                                            running = query_job_running,
                                            ok = query_job_ok,
                                            error = query_job_error,
                                            misfired = query_job_misfired,
                                            query_distinct_count = query_distinct_count,
                                            long_running_count = long_running_count,
                                            next_num=next_num,
                                            prev_num=prev_num
                                            )

@app.route('/search_dashboard', methods=['GET', 'POST'])
def search_dashboard():
    page = request.args.get('page', 1, type=int)
    query_job_running = Job_Monitoring.query.filter(Job_Monitoring.status == 'RUNNING').count()
    query_job_ok = Job_Monitoring.query.filter(Job_Monitoring.status == 'OK').count()
    query_job_error = Job_Monitoring.query.filter(Job_Monitoring.status == 'ERROR').count()
    query_job_misfired = Job_Monitoring.query.filter(Job_Monitoring.status == 'MISFIRED').count()

    global search, tag
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)


    search_string = Job_Monitoring.query.filter(or_(Job_Monitoring.starttime.like(search), 
                                                    Job_Monitoring.duration_mins.like(search), 
                                                    Job_Monitoring.tasklabel.like(search), 
                                                    Job_Monitoring.id.like(search), 
                                                    Job_Monitoring.status.like(search), ))\
                    .paginate(page=page, per_page=50)

    search_next_num = url_for('search_dashboard', page=search_string.next_num) \
        if search_string.has_next else None
    search_prev_num = url_for('search_dashboard', page=search_string.prev_num) \
        if search_string.has_prev else None

    return render_template('dashboard_search.html', query=search_string, 
                                        running = query_job_running,
                                        tag=tag,
                                        ok = query_job_ok,
                                        error = query_job_error,
                                        misfired = query_job_misfired,
                                        search=search,
                                        next_num=search_next_num,
                                        prev_num=search_prev_num
                                        )

@app.route('/datetime_dashboard', methods=['GET', 'POST'])
def datetime_dashboard():
    page = request.args.get('page', 1, type=int)
    query_job_running = Job_Monitoring.query.filter(Job_Monitoring.status == 'RUNNING').count()
    query_job_ok = Job_Monitoring.query.filter(Job_Monitoring.status == 'OK').count()
    query_job_error = Job_Monitoring.query.filter(Job_Monitoring.status == 'ERROR').count()
    query_job_misfired = Job_Monitoring.query.filter(Job_Monitoring.status == 'MISFIRED').count()

    global mindate, maxdate, minDate, maxDate
    if request.method == 'POST' and 'datetimepickermin' in request.form or 'datetimepickermax' in request.form:
        minDate = request.form["datetimepickermin"]
        maxDate = request.form["datetimepickermax"]
        mindate = "{}%".format(minDate)
        maxdate = "{}%".format(maxDate)

    search_string = Job_Monitoring.query.filter(or_(Job_Monitoring.starttime.like(mindate), Job_Monitoring.starttime.like(maxdate)))\
                       .paginate(page=page, per_page=50, error_out=False)
    
    search_next_num = url_for('datetime_dashboard', page=search_string.next_num) \
        if search_string.has_next else None
    search_prev_num = url_for('datetime_dashboard', page=search_string.prev_num) \
        if search_string.has_prev else None

    return render_template('dashboard_search.html', query=search_string, 
                                        minDate=minDate,
                                        maxDate=maxDate,
                                        tag=tag,
                                        running = query_job_running,
                                        ok = query_job_ok,
                                        error = query_job_error,
                                        misfired = query_job_misfired,
                                        next_num=search_next_num,
                                        prev_num=search_prev_num
                                        )

@app.route("/dashboard/<string:status>", methods=['GET', 'POST'])
def status_job(status):
    page = request.args.get('page', 1, type=int)
    query_job_running = Job_Monitoring.query.filter(Job_Monitoring.status == 'RUNNING').count()
    query_job_ok = Job_Monitoring.query.filter(Job_Monitoring.status == 'OK').count()
    query_job_error = Job_Monitoring.query.filter(Job_Monitoring.status == 'ERROR').count()
    query_job_misfired = Job_Monitoring.query.filter(Job_Monitoring.status == 'MISFIRED').count()

    job_status = Job_Monitoring.query.filter(Job_Monitoring.status == status)\
                                        .order_by(Job_Monitoring.starttime.desc())\
                                        .paginate(page=page, per_page=50)      

    return render_template('dashboard_status.html', query=job_status,
                                            running = query_job_running,
                                            ok = query_job_ok,
                                            error = query_job_error,
                                            misfired = query_job_misfired,
                                            status=status)





@app.route('/bca_monitoring', methods=['GET', 'POST'])
def bca_monitoring():
    page = request.args.get('page', 1, type=int)
    # results = session.query(bca_monitoring_table).all()
    bca_query = Job_BCA.query.order_by(Job_BCA.RunDate.desc()).paginate(page=page, per_page=50)


    return render_template('bca_monitoring.html', bca_query = bca_query)
    # return render_template('bca_monitoring.html')

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



# JS CHARTS
@app.route('/get_bca_monitoring', methods=['GET'])
def get_bca_monitoring():
    results = session.query(bca_monitoring_table).all()
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

@app.route('/get_job_monitoring', methods=['GET'])
def get_job_monitoring():
    # results = session.query(job_monitoring_table).all()

    job_status = []
    job_Label = ['RUNNING', 'COMPLETED', 'ERROR', 'MISFIRED']

    query_job_running = Job_Monitoring.query.filter(Job_Monitoring.status == 'RUNNING').count()
    query_job_ok = Job_Monitoring.query.filter(Job_Monitoring.status == 'OK').count()
    query_job_error = Job_Monitoring.query.filter(Job_Monitoring.status == 'ERROR').count()
    query_job_misfired = Job_Monitoring.query.filter(Job_Monitoring.status == 'MISFIRED').count()

    job_status.append(query_job_running)
    job_status.append(query_job_ok)
    job_status.append(query_job_error)
    job_status.append(query_job_misfired)

    result_set = {
        "job_status": job_status,
        "job_Label": job_Label,

    }

    return jsonify(result_set)

# EXPORTING FILES
@app.route('/generate_csv', methods=['GET'])
def generate_csv():
    result = Job_Monitoring.query.order_by(Job_Monitoring.starttime.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)

    line = ['Job Start Time, Duration in minutes, Task Labels, Job ID, Status']
    writer.writerow(line)

    for row in result:
        line = [str(row.starttime) + ',' + str(row.duration_mins) + ',' + str(row.tasklabel) + ',' + str(row.id) + ',' + str(row.status)]
        writer.writerow(line)
    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=Talend_Job_Report.csv"})

@app.route('/generate_excel', methods=['GET'])
def generate_excel():
    result = Job_Monitoring.query.order_by(Job_Monitoring.starttime.desc()).all()

    #output in bytes
    output = io.BytesIO()
    #create WorkBook object
    workbook = Workbook()
    #add a sheet
    sh = workbook.create_sheet('Talend Job Report')
    #add headers
    sh.append(['Job Start Time', 'Duration in minutes', 'Task Labels', 'Job ID', 'Status'])

    for row in result:
        sh.append([
            str(row.starttime),
            str(row.duration_mins),
            str(row.tasklabel),
            str(row.id),
            str(row.status)
        ])

    workbook_name = "Talend Job Report"
    workbook.save(output)
    output.seek(0)

    return Response(output, mimetype="application/openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition":"attachment;filename=Talend_Job_Report.xlsx"})


@app.route('/get_jobs', methods=['GET'])
def get_jobs():
    # query_string = Job_Monitoring.query.order_by(Job_Monitoring.starttime.desc()).paginate(page=page, per_page=50)

    per_job = []
    # global mindate
    query_distinct = Job_Monitoring.query.with_entities(Job_Monitoring.tasklabel).distinct()
    for r in query_distinct:
        print(r)
        distinct_query = Job_Monitoring.query.filter(Job_Monitoring.tasklabel == r).all()
        for status in distinct_query:
            # print(status.status) 
            per_job.append([
                str(status.tasklabel),
                str(status.starttime),
                str(status.duration_mins),                
                str(status.id),
                str(status.status)
            ])
        
    print(per_job)

    result_set = {
        "job_status": per_job,
    }

    return jsonify(result_set)

@app.route('/dashboard_jobs', methods=['GET'])
def dashboard_jobs():
    # query_string = Job_Monitoring.query.order_by(Job_Monitoring.starttime.desc()).paginate(page=page, per_page=50)

    # per_job = []
    # global mindate
    query_distinct = Job_Monitoring.query.with_entities(Job_Monitoring.tasklabel).distinct().paginate(page=page, per_page=50)

    return render_template('dashboard_jobs.html', query=query_distinct)



# LONG RUNNING JOBS TAB
@app.route('/job_long_running', methods=['GET', 'POST'])
def job_long_running():
    page = request.args.get('page', 1, type=int)

    long_running = Job_Monitoring.query.filter(Job_Monitoring.duration_mins >= 30) \
                    .order_by(Job_Monitoring.starttime.desc()).paginate(page=page, per_page=50)

    query_job_running = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'RUNNING', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_ok = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'OK', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_error = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'ERROR', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_misfired = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'MISFIRED', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()

    long_next_num = url_for('job_long_running', page=long_running.next_num) \
        if long_running.has_next else None
    long_prev_num = url_for('job_long_running', page=long_running.prev_num) \
        if long_running.has_prev else None

    return render_template("dashboard_longrunningjobs.html", query=long_running,
                                                            running = query_job_running,
                                                            ok = query_job_ok,
                                                            error = query_job_error,
                                                            misfired = query_job_misfired,
                                                            next_num=long_next_num,
                                                            prev_num=long_prev_num
                                                            )

@app.route('/get_long_running_jobs', methods=['GET'])
def get_long_running_jobs():
    job_status = []
    job_Label = ['RUNNING', 'COMPLETED', 'ERROR', 'MISFIRED']

    query_job_running = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'RUNNING', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_ok = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'OK', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_error = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'ERROR', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_misfired = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'MISFIRED', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()

    job_status.append(query_job_running)
    job_status.append(query_job_ok)
    job_status.append(query_job_error)
    job_status.append(query_job_misfired)

    result_set = {
        "job_status": job_status,
        "job_Label": job_Label,

    }

    return jsonify(result_set)

@app.route('/lrj_generate_csv', methods=['GET', 'POST'])
def lrj_generate_csv():

    global search, tag
    if request.method == 'POST' and 'status' in request.form:
        status = request.form["status"]
        search = "%{}%".format(status)

    if status == 'ALL':
        result = Job_Monitoring.query.filter(Job_Monitoring.duration_mins >= 30).all()
    else:
        result = Job_Monitoring.query.filter(and_(Job_Monitoring.status == status, 
                                                        Job_Monitoring.duration_mins >= 30 )).all()
    # result = Job_Monitoring.query.filter(Job_Monitoring.duration_mins >= 30).all()
    # result = Job_Monitoring.query.order_by(Job_Monitoring.starttime.desc()).all()
    # print(status)
    output = io.StringIO()
    writer = csv.writer(output)

    line = ['Job Start Time, Duration in minutes, Task Labels, Job ID, Status']
    writer.writerow(line)

    for row in result:
        line = [str(row.starttime) + ',' + str(row.duration_mins) + ',' + str(row.tasklabel) + ',' + str(row.id) + ',' + str(row.status)]
        writer.writerow(line)
    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=Talend_Job_Report.csv"})

@app.route('/lrj_generate_excel', methods=['GET', 'POST'])
def lrj_generate_excel():
    global search, tag
    if request.method == 'POST' and 'status' in request.form:
        status = request.form["status"]
        search = "%{}%".format(status)

    if status == 'ALL':
        result = Job_Monitoring.query.filter(Job_Monitoring.duration_mins >= 30).all()
    else:
        result = Job_Monitoring.query.filter(and_(Job_Monitoring.status == status, 
                                                        Job_Monitoring.duration_mins >= 30 )).all()

    #output in bytes
    output = io.BytesIO()
    #create WorkBook object
    workbook = Workbook()
    #add a sheet
    sh = workbook.create_sheet('Talend Job Report')
    #add headers
    sh.append(['Job Start Time', 'Duration in minutes', 'Task Labels', 'Job ID', 'Status'])

    for row in result:
        sh.append([
            str(row.starttime),
            str(row.duration_mins),
            str(row.tasklabel),
            str(row.id),
            str(row.status)
        ])

    workbook_name = "Talend Job Report"
    workbook.save(output)
    output.seek(0)

    return Response(output, mimetype="application/openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition":"attachment;filename=Talend_Job_Report.xlsx"})


#DQ CHECKS
@app.route('/dq_checks', methods=['GET', 'POST'])
def dq_checks():
    variance_com = session.query(func.sum(manifest_hive_monitoring.variance)).filter(manifest_hive_monitoring.cdr_type=="com").scalar()
    variance_vou = session.query(func.sum(manifest_hive_monitoring.variance)).filter(manifest_hive_monitoring.cdr_type=="vou").scalar()
    variance_first = session.query(func.sum(manifest_hive_monitoring.variance)).filter(manifest_hive_monitoring.cdr_type=="first").scalar()
    variance_mon = session.query(func.sum(manifest_hive_monitoring.variance)).filter(manifest_hive_monitoring.cdr_type=="mon").scalar()
    variance_cm = session.query(func.sum(manifest_hive_monitoring.variance)).filter(manifest_hive_monitoring.cdr_type=="cm").scalar()
    variance_adj = session.query(func.sum(manifest_hive_monitoring.variance)).filter(manifest_hive_monitoring.cdr_type=="adj").scalar()
    
    print(variance_com)
    print(str(variance_vou))
    print(str(variance_first))
    print(str(variance_mon))
    print(str(variance_cm))
    print(str(variance_adj))

    return render_template('dq_checks.html', variance_com = variance_com,
                                                variance_vou = variance_vou,
                                                variance_first = variance_first,
                                                variance_mon = variance_mon,
                                                variance_cm = variance_cm,
                                                variance_adj = variance_adj)

@app.route('/get_dqchecks_js', methods=['GET'])
def get_dqchecks_js():

    results = session.query(manifest_hive_monitoring).all()
    com_manifest = []
    com_t1 = []
    com_variance = []
    vou_manifest = []
    vou_t1 = []
    vou_variance = []
    first_manifest = []
    first_t1 = []
    first_variance = []
    mon_manifest = []
    mon_t1 = []
    mon_variance = []
    cm_manifest = []
    cm_t1 = []
    cm_variance = []
    adj_manifest = []
    adj_t1 = []
    adj_variance = []

    for r in results:
        if r.cdr_type == "com":
            com_manifest.append(str(r.ocs_manifest))
            com_t1.append(str(r.t1_hive))
            com_variance.append(str(r.variance))
        elif r.cdr_type == "vou":
            vou_manifest.append(str(r.ocs_manifest))
            vou_t1.append(str(r.t1_hive))
            vou_variance.append(str(r.variance))
        elif r.cdr_type == "first":
            first_manifest.append(str(r.ocs_manifest))
            first_t1.append(str(r.t1_hive))
            first_variance.append(str(r.variance))
        elif r.cdr_type == "mon":
            mon_manifest.append(str(r.ocs_manifest))
            mon_t1.append(str(r.t1_hive))
            mon_variance.append(str(r.variance))
        elif r.cdr_type == "cm":
            cm_manifest.append(str(r.ocs_manifest))
            cm_t1.append(str(r.t1_hive))
            cm_variance.append(str(r.variance))
        elif r.cdr_type == "adj":
            adj_manifest.append(str(r.ocs_manifest))
            adj_t1.append(str(r.t1_hive))
            adj_variance.append(str(r.variance))

    result_set = {
        "com_manifest": com_manifest,
        "com_t1": com_t1,
        "com_variance": com_variance,
        "vou_manifest": vou_manifest,
        "vou_t1": vou_t1,
        "vou_variance": vou_variance,
        "first_manifest": first_manifest,
        "first_t1": first_t1,
        "first_variance": first_variance,
        "mon_manifest": mon_manifest,
        "mon_t1": mon_t1,
        "mon_variance": mon_variance,
        "cm_manifest": cm_manifest,
        "cm_t1": cm_t1,
        "cm_variance": cm_variance,
        "adj_manifest": adj_manifest,
        "adj_t1": adj_t1,
        "adj_variance": adj_variance,

    }

    return jsonify(result_set)