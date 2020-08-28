from flask import render_template, request, url_for, jsonify

from smartdashboard import app,  session, bca_monitoring_table, manifest_hive_monitoring, manifest_oracle_monitoring
from smartdashboard.models import Job_Monitoring, Job_BCA, Dly_Usagetype, Dly_Prp_Acct, Dly_Pcodes, topsku_prod, topsku_talend
from smartdashboard.forms import Search
from smartdashboard.utils import time_to_seconds, init_list

from sqlalchemy import or_, and_
from sqlalchemy.sql import func
from flask import jsonify, Response

from datetime import datetime
from datetime import date

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






# JS CHARTS
@app.route('/get_job_monitoring', methods=['GET'])
def get_job_monitoring():
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
@app.route('/long_running_job', methods=['GET', 'POST'])
def long_running_job():
    page = request.args.get('page', 1, type=int)

    long_running = Job_Monitoring.query.filter(Job_Monitoring.duration_mins >= 30) \
                    .order_by(Job_Monitoring.starttime.desc()).paginate(page=page, per_page=50)

    get_time = Job_Monitoring.query.filter(Job_Monitoring.duration_mins >= 30) \
                    .order_by(Job_Monitoring.starttime.asc()).all()
    global time
    for r in get_time:
        time = str(r.starttime)


    query_job_running = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'RUNNING', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_ok = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'OK', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_error = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'ERROR', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_misfired = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'MISFIRED', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()

    long_next_num = url_for('long_running_job', page=long_running.next_num) \
        if long_running.has_next else None
    long_prev_num = url_for('long_running_job', page=long_running.prev_num) \
        if long_running.has_prev else None

    return render_template("longrunningjobs.html", query=long_running,
                                                            running = query_job_running,
                                                            ok = query_job_ok,
                                                            error = query_job_error,
                                                            misfired = query_job_misfired,
                                                            next_num=long_next_num,
                                                            prev_num=long_prev_num,
                                                            time = time
                                                            )

@app.route('/lrj_js', methods=['GET'])
def lrj_js():
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

@app.route('/lrj_search', methods=['GET', 'POST'])
def lrj_search():
    page = request.args.get('page', 1, type=int)

    query_job_running = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'RUNNING', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_ok = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'OK', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_error = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'ERROR', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_misfired = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'MISFIRED', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()

    global search, tag
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)


    search_string = Job_Monitoring.query.filter(or_(and_(Job_Monitoring.duration_mins >= 30, Job_Monitoring.starttime.like(search)), 
                                                    and_(Job_Monitoring.duration_mins >= 30, Job_Monitoring.duration_mins.like(search)), 
                                                    and_(Job_Monitoring.duration_mins >= 30, Job_Monitoring.tasklabel.like(search)), 
                                                    and_(Job_Monitoring.duration_mins >= 30, Job_Monitoring.id.like(search)), 
                                                    and_(Job_Monitoring.duration_mins >= 30, Job_Monitoring.status.like(search)), 
                                                    ))\
                                                        .order_by(Job_Monitoring.starttime.desc()).paginate(page=page, per_page=50)


    search_next_num = url_for('lrj_search', page=search_string.next_num) \
        if search_string.has_next else None
    search_prev_num = url_for('lrj_search', page=search_string.prev_num) \
        if search_string.has_prev else None

    return render_template('longrunningjob_search.html', query=search_string, 
                                        running = query_job_running,
                                        tag=tag,
                                        ok = query_job_ok,
                                        error = query_job_error,
                                        misfired = query_job_misfired,
                                        search=search,
                                        next_num=search_next_num,
                                        prev_num=search_prev_num
                                        )

@app.route('/lrj_datetime', methods=['GET', 'POST'])
def lrj_datetime():
    page = request.args.get('page', 1, type=int)
    query_job_running = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'RUNNING', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_ok = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'OK', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_error = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'ERROR', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_misfired = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'MISFIRED', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()


    global mindate, maxdate, minDate, maxDate
    if request.method == 'POST' and 'datetimepickermin' in request.form or 'datetimepickermax' in request.form:
        minDate = request.form["datetimepickermin"]
        maxDate = request.form["datetimepickermax"]
        mindate = "{}%".format(minDate)
        maxdate = "{}%".format(maxDate)

    search_string = Job_Monitoring.query.filter(or_(and_(Job_Monitoring.duration_mins >= 30, Job_Monitoring.starttime.like(mindate)), 
                                                    and_(Job_Monitoring.duration_mins >= 30, Job_Monitoring.starttime.like(maxdate))
                                                    ))\
                                                        .order_by(Job_Monitoring.starttime.desc()).paginate(page=page, per_page=50, error_out=False)
    
    search_next_num = url_for('lrj_datetime', page=search_string.next_num) \
        if search_string.has_next else None
    search_prev_num = url_for('lrj_datetime', page=search_string.prev_num) \
        if search_string.has_prev else None

    return render_template('longrunningjob_search.html', query=search_string, 
                                        minDate=minDate,
                                        maxDate=maxDate,
                                        running = query_job_running,
                                        ok = query_job_ok,
                                        error = query_job_error,
                                        misfired = query_job_misfired,
                                        next_num=search_next_num,
                                        prev_num=search_prev_num
                                        )

@app.route("/long_running_job/<string:status>", methods=['GET', 'POST'])
def status_job(status):
    page = request.args.get('page', 1, type=int)
    query_job_running = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'RUNNING', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_ok = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'OK', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_error = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'ERROR', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_misfired = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'MISFIRED', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()

    job_status = Job_Monitoring.query.filter(and_(Job_Monitoring.duration_mins >= 30, Job_Monitoring.status == status))\
                                        .order_by(Job_Monitoring.starttime.desc()).paginate(page=page, per_page=50)      

    return render_template('longrunningjob_status.html', query=job_status,
                                            running = query_job_running,
                                            ok = query_job_ok,
                                            error = query_job_error,
                                            misfired = query_job_misfired,
                                            status=status)










#DQ CHECKS - MANIFEST VS TI-HIVE
@app.route('/dq_checks', methods=['GET', 'POST'])
def dq_checks():

    variance_com = session.query(func.sum(manifest_hive_monitoring.variance)).filter(and_(manifest_hive_monitoring.cdr_type =="com",manifest_hive_monitoring.file_date == date.today())).scalar()
    variance_vou = session.query(func.sum(manifest_hive_monitoring.variance)).filter(and_(manifest_hive_monitoring.cdr_type =="vou",manifest_hive_monitoring.file_date == date.today())).scalar()
    variance_first = session.query(func.sum(manifest_hive_monitoring.variance)).filter(and_(manifest_hive_monitoring.cdr_type =="first",manifest_hive_monitoring.file_date == date.today())).scalar()
    variance_mon = session.query(func.sum(manifest_hive_monitoring.variance)).filter(and_(manifest_hive_monitoring.cdr_type =="mon",manifest_hive_monitoring.file_date == date.today())).scalar()
    variance_cm = session.query(func.sum(manifest_hive_monitoring.variance)).filter(and_(manifest_hive_monitoring.cdr_type =="cm",manifest_hive_monitoring.file_date == date.today())).scalar()
    variance_adj = session.query(func.sum(manifest_hive_monitoring.variance)).filter(and_(manifest_hive_monitoring.cdr_type =="adj",manifest_hive_monitoring.file_date == date.today())).scalar()

    # print(variance_com)
    # print(str(variance_vou))
    # print(str(variance_first))
    # print(str(variance_mon))
    # print(str(variance_cm))
    # print(str(variance_adj))

    return render_template('dq_checks.html', variance_com = variance_com,
                                                variance_vou = variance_vou,
                                                variance_first = variance_first,
                                                variance_mon = variance_mon,
                                                variance_cm = variance_cm,
                                                variance_adj = variance_adj)

@app.route('/get_dqchecks_js', methods=['GET','POST'])
def get_dqchecks_js():
    if request.method == "POST":
        query_date = request.form["cdr_date"]
    else:
        query_date = date.today()

    results = session.query(manifest_hive_monitoring).filter(manifest_hive_monitoring.file_date == query_date)
    com_manifest = init_list()
    com_t1 = init_list()
    com_variance = init_list()
    vou_manifest = init_list()
    vou_t1 = init_list()
    vou_variance = init_list()
    first_manifest = init_list()
    first_t1 = init_list()
    first_variance = init_list()
    mon_manifest = init_list()
    mon_t1 = init_list()
    mon_variance = init_list()
    cm_manifest = init_list()
    cm_t1 = init_list()
    cm_variance = init_list()
    adj_manifest = init_list()
    adj_t1 = init_list()
    adj_variance = init_list()

    for r in results:
        if r.cdr_type == "com":
            com_manifest[r.processing_hour] = (str(r.ocs_manifest))
            com_t1[r.processing_hour] = (str(r.t1_hive))
            com_variance[r.processing_hour] = (str(r.variance))
        elif r.cdr_type == "vou":
            vou_manifest[r.processing_hour] = (str(r.ocs_manifest))
            vou_t1[r.processing_hour] = (str(r.t1_hive))
            vou_variance[r.processing_hour] = (str(r.variance))
        elif r.cdr_type == "first":
            first_manifest[r.processing_hour] = (str(r.ocs_manifest))
            first_t1[r.processing_hour] = (str(r.t1_hive))
            first_variance[r.processing_hour] = (str(r.variance))
        elif r.cdr_type == "mon":
            mon_manifest[r.processing_hour] = (str(r.ocs_manifest))
            mon_t1[r.processing_hour] = (str(r.t1_hive))
            mon_variance[r.processing_hour] = (str(r.variance))
        elif r.cdr_type == "cm":
            cm_manifest[r.processing_hour] = (str(r.ocs_manifest))
            cm_t1[r.processing_hour] = (str(r.t1_hive))
            cm_variance[r.processing_hour] = (str(r.variance))
        elif r.cdr_type == "adj":
            adj_manifest[r.processing_hour] = (str(r.ocs_manifest))
            adj_t1[r.processing_hour] = (str(r.t1_hive))
            adj_variance[r.processing_hour] = (str(r.variance))

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

@app.route('/dq_checks_search_hive', methods=['POST'])
def dq_checks_search_hive():
    if request.method == "POST":
        query_date = request.form["date"]
        variance_com = session.query(func.sum(manifest_hive_monitoring.variance)).filter(and_(manifest_hive_monitoring.cdr_type =="com",manifest_hive_monitoring.file_date == query_date)).scalar()
        variance_vou = session.query(func.sum(manifest_hive_monitoring.variance)).filter(and_(manifest_hive_monitoring.cdr_type =="vou",manifest_hive_monitoring.file_date == query_date)).scalar()
        variance_first = session.query(func.sum(manifest_hive_monitoring.variance)).filter(and_(manifest_hive_monitoring.cdr_type =="first",manifest_hive_monitoring.file_date == query_date)).scalar()
        variance_mon = session.query(func.sum(manifest_hive_monitoring.variance)).filter(and_(manifest_hive_monitoring.cdr_type =="mon",manifest_hive_monitoring.file_date == query_date)).scalar()
        variance_cm = session.query(func.sum(manifest_hive_monitoring.variance)).filter(and_(manifest_hive_monitoring.cdr_type =="cm",manifest_hive_monitoring.file_date == query_date)).scalar()
        variance_adj = session.query(func.sum(manifest_hive_monitoring.variance)).filter(and_(manifest_hive_monitoring.cdr_type =="adj",manifest_hive_monitoring.file_date == query_date)).scalar()

    result_set = {
        "variance_com": str(variance_com),
        "variance_vou": str(variance_vou),
        "variance_first": str(variance_first),
        "variance_mon": str(variance_mon),
        "variance_cm": str(variance_cm),
        "variance_adj": str(variance_adj)
    }

    return jsonify(result_set)

#DQ CHECKS - MANIFEST VS TI-ORACLE
@app.route('/dq_checks_2', methods=['GET', 'POST'])
def dq_checks_2():
    variance_com = session.query(func.sum(manifest_oracle_monitoring.variance)).filter(and_(manifest_oracle_monitoring.cdr_type =="com",manifest_oracle_monitoring.file_date == date.today())).scalar()
    variance_vou = session.query(func.sum(manifest_oracle_monitoring.variance)).filter(and_(manifest_oracle_monitoring.cdr_type =="vou",manifest_oracle_monitoring.file_date == date.today())).scalar()
    variance_first = session.query(func.sum(manifest_oracle_monitoring.variance)).filter(and_(manifest_oracle_monitoring.cdr_type =="first",manifest_oracle_monitoring.file_date == date.today())).scalar()
    variance_mon = session.query(func.sum(manifest_oracle_monitoring.variance)).filter(and_(manifest_oracle_monitoring.cdr_type =="mon",manifest_oracle_monitoring.file_date == date.today())).scalar()
    variance_cm = session.query(func.sum(manifest_oracle_monitoring.variance)).filter(and_(manifest_oracle_monitoring.cdr_type =="cm",manifest_oracle_monitoring.file_date == date.today())).scalar()
    variance_adj = session.query(func.sum(manifest_oracle_monitoring.variance)).filter(and_(manifest_oracle_monitoring.cdr_type =="adj",manifest_oracle_monitoring.file_date == date.today())).scalar()

    # print(variance_com)
    # print(str(variance_vou))
    # print(str(variance_first))
    # print(str(variance_mon))
    # print(str(variance_cm))
    # print(str(variance_adj))

    return render_template('dq_checks_2.html', variance_com = variance_com,
                                                variance_vou = variance_vou,
                                                variance_first = variance_first,
                                                variance_mon = variance_mon,
                                                variance_cm = variance_cm,
                                                variance_adj = variance_adj
                                                )

@app.route('/get_dqchecks2_js', methods=['GET','POST'])
def get_dqchecks2_js():
    if request.method == "POST":
        query_date = request.form["cdr_date"]
    else:
        query_date = date.today()
    
    results = session.query(manifest_oracle_monitoring).filter(manifest_oracle_monitoring.file_date == query_date)
    com_manifest = init_list()
    com_t1 = init_list()
    com_variance = init_list()
    vou_manifest = init_list()
    vou_t1 = init_list()
    vou_variance = init_list()
    first_manifest = init_list()
    first_t1 = init_list()
    first_variance = init_list()
    mon_manifest = init_list()
    mon_t1 = init_list()
    mon_variance = init_list()
    cm_manifest = init_list()
    cm_t1 = init_list()
    cm_variance = init_list()
    adj_manifest = init_list()
    adj_t1 = init_list()
    adj_variance = init_list()

    for r in results:
        if r.cdr_type == "com":
            com_manifest[r.processing_hour] = (str(r.ocs_manifest))
            com_t1[r.processing_hour] = (str(r.t1_oracle))
            com_variance[r.processing_hour] = (str(r.variance))
        elif r.cdr_type == "vou":
            vou_manifest[r.processing_hour] = (str(r.ocs_manifest))
            vou_t1[r.processing_hour] = (str(r.t1_oracle))
            vou_variance[r.processing_hour] = (str(r.variance))
        elif r.cdr_type == "first":
            first_manifest[r.processing_hour] = (str(r.ocs_manifest))
            first_t1[r.processing_hour] = (str(r.t1_oracle))
            first_variance[r.processing_hour] = (str(r.variance))
        elif r.cdr_type == "mon":
            mon_manifest[r.processing_hour] = (str(r.ocs_manifest))
            mon_t1[r.processing_hour] = (str(r.t1_oracle))
            mon_variance[r.processing_hour] = (str(r.variance))
        elif r.cdr_type == "cm":
            cm_manifest[r.processing_hour] = (str(r.ocs_manifest))
            cm_t1[r.processing_hour] = (str(r.t1_oracle))
            cm_variance[r.processing_hour] = (str(r.variance))
        elif r.cdr_type == "adj":
            adj_manifest[r.processing_hour] = (str(r.ocs_manifest))
            adj_t1[r.processing_hour] = (str(r.t1_oracle))
            adj_variance[r.processing_hour] = (str(r.variance))
    
    # results.close()

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

@app.route('/dq_checks_search_oracle', methods=['POST'])
def dq_checks_search_oracle():
    if request.method == "POST":
        query_date = request.form["date"]
        variance_com = session.query(func.sum(manifest_oracle_monitoring.variance)).filter(and_(manifest_oracle_monitoring.cdr_type =="com",manifest_oracle_monitoring.file_date == query_date)).scalar()
        variance_vou = session.query(func.sum(manifest_oracle_monitoring.variance)).filter(and_(manifest_oracle_monitoring.cdr_type =="vou",manifest_oracle_monitoring.file_date == query_date)).scalar()
        variance_first = session.query(func.sum(manifest_oracle_monitoring.variance)).filter(and_(manifest_oracle_monitoring.cdr_type =="first",manifest_oracle_monitoring.file_date == query_date)).scalar()
        variance_mon = session.query(func.sum(manifest_oracle_monitoring.variance)).filter(and_(manifest_oracle_monitoring.cdr_type =="mon",manifest_oracle_monitoring.file_date == query_date)).scalar()
        variance_cm = session.query(func.sum(manifest_oracle_monitoring.variance)).filter(and_(manifest_oracle_monitoring.cdr_type =="cm",manifest_oracle_monitoring.file_date == query_date)).scalar()
        variance_adj = session.query(func.sum(manifest_oracle_monitoring.variance)).filter(and_(manifest_oracle_monitoring.cdr_type =="adj",manifest_oracle_monitoring.file_date == query_date)).scalar()

    result_set = {
        "variance_com": str(variance_com),
        "variance_vou": str(variance_vou),
        "variance_first": str(variance_first),
        "variance_mon": str(variance_mon),
        "variance_cm": str(variance_cm),
        "variance_adj": str(variance_adj)
    }

    return jsonify(result_set)

# BCA MONITORING TAB
@app.route('/bca_monitoring', methods=['GET', 'POST'])
def bca_monitoring():
    page = request.args.get('page', 1, type=int)
    bca_query = Job_BCA.query.order_by(Job_BCA.RunDate.desc()).paginate(page=page, per_page=50)


    return render_template('bca_monitoring.html', bca_query = bca_query)

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