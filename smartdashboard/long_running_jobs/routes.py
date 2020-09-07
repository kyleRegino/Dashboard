from flask import render_template, request, url_for, jsonify, Response, Blueprint
from smartdashboard.models import Job_Monitoring
from sqlalchemy import or_, and_
from sqlalchemy.sql import func
import io, csv
from openpyxl import Workbook
from smartdashboard.utils import number_formatter

from datetime import datetime
from datetime import date

lrj_blueprint = Blueprint('lrj_blueprint', __name__)

@lrj_blueprint.route('/long_running_job', methods=['GET', 'POST'])
def long_running_job():
    page = request.args.get('page', 1, type=int)

    long_running = Job_Monitoring.query.filter(and_(Job_Monitoring.duration_mins >= 30, Job_Monitoring.status == 'RUNNING')) \
                    .order_by(Job_Monitoring.starttime.desc()).paginate(page=page, per_page=50)

    get_time = Job_Monitoring.query.filter(Job_Monitoring.duration_mins >= 30) \
                    .order_by(Job_Monitoring.starttime.desc()).first()

    query_job_running = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'RUNNING', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_ok = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'OK', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_error = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'ERROR', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()
    query_job_misfired = Job_Monitoring.query.filter(and_(Job_Monitoring.status == 'MISFIRED', 
                                                    Job_Monitoring.duration_mins >= 30 )).count()

    long_next_num = url_for('lrj_blueprint.long_running_job', page=long_running.next_num) \
        if long_running.has_next else None
    long_prev_num = url_for('lrj_blueprint.long_running_job', page=long_running.prev_num) \
        if long_running.has_prev else None

    return render_template("longrunningjobs.html", query=long_running,
                                                            running = number_formatter(query_job_running),
                                                            ok = query_job_ok,
                                                            error = query_job_error,
                                                            misfired = query_job_misfired,
                                                            next_num=long_next_num,
                                                            prev_num=long_prev_num,
                                                            time = get_time
                                                            )

@lrj_blueprint.route('/lrj_generate_csv', methods=['GET', 'POST'])
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

@lrj_blueprint.route('/lrj_generate_excel', methods=['GET', 'POST'])
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

@lrj_blueprint.route('/lrj_search', methods=['GET', 'POST'])
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


    search_next_num = url_for('lrj_blueprint.lrj_search', page=search_string.next_num) \
        if search_string.has_next else None
    search_prev_num = url_for('lrj_blueprint.lrj_search', page=search_string.prev_num) \
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

@lrj_blueprint.route('/lrj_datetime', methods=['GET', 'POST'])
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
    
    search_next_num = url_for('lrj_blueprint.lrj_datetime', page=search_string.next_num) \
        if search_string.has_next else None
    search_prev_num = url_for('lrj_blueprint.lrj_datetime', page=search_string.prev_num) \
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

@lrj_blueprint.route("/long_running_job/<string:status>", methods=['GET', 'POST'])
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

@lrj_blueprint.route('/lrj_js', methods=['GET'])
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