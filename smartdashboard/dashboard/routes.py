from flask import render_template, request, url_for, jsonify, Response, Blueprint
from smartdashboard.models import Job_Monitoring
from datetime import date

dashboard_blueprint = Blueprint('dashboard_blueprint', __name__)

@dashboard_blueprint.route('/')
@dashboard_blueprint.route('/dashboard', methods=['GET', 'POST'])
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

    next_num = url_for('dashboard_blueprint.dashboard', page=query_string.next_num) \
            if query_string.has_next else None
    prev_num = url_for('dashboard_blueprint.dashboard', page=query_string.prev_num) \
        if query_string.has_prev else None

    if request.method == 'POST' and 'datetimepickermin' in request.form or 'datetimepickermax' in request.form:
        minDate = request.form["datetimepickermin"]
        maxDate = request.form["datetimepickermax"]
        min = "{}%".format(minDate)
        max = "{}%".format(maxDate)
        print(min)
        print(max)

    thedate = date.today()

    return render_template("dashboard.html", query = query_string,
                                            running = query_job_running,
                                            ok = query_job_ok,
                                            error = query_job_error,
                                            misfired = query_job_misfired,
                                            query_distinct_count = query_distinct_count,
                                            long_running_count = long_running_count,
                                            next_num=next_num,
                                            prev_num=prev_num,
                                            date=thedate
                                            )

@dashboard_blueprint.route('/get_job_monitoring', methods=['GET'])
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