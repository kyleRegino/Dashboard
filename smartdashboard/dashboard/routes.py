from flask import render_template, request, url_for, jsonify, Response, Blueprint
from smartdashboard.models import Job_Monitoring
from smartdashboard import db, manifest_hive_monitoring, manifest_oracle_monitoring, pending
from datetime import date
from datetime import datetime
from sqlalchemy import or_, and_
from smartdashboard.utils import number_formatter

dashboard_blueprint = Blueprint('dashboard_blueprint', __name__)

# @dashboard_blueprint.route('/')
@dashboard_blueprint.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    page = request.args.get('page', 1, type=int)
    query_job_running = Job_Monitoring.query.filter(Job_Monitoring.status == 'RUNNING').count()
    query_distinct_count = Job_Monitoring.query.with_entities(Job_Monitoring.tasklabel).distinct().count()
    long_running_count = Job_Monitoring.query.filter(and_(Job_Monitoring.duration_mins >= 30, Job_Monitoring.status == 'RUNNING')).count()
    pendings = db.session.query(pending).all()
    pending_hdfs = []
    time_p_hdfs = None
    pending_hive = []
    time_p_hive = None
    # TIME
    time_overall = Job_Monitoring.query.order_by(Job_Monitoring.starttime.desc()).first()
    time_lrj = Job_Monitoring.query.filter(Job_Monitoring.duration_mins >= 30) \
                    .order_by(Job_Monitoring.starttime.desc()).first()
    time_hive = db.session.query(manifest_hive_monitoring).order_by(manifest_hive_monitoring.file_date.desc()).first()
    time_oracle = db.session.query(manifest_oracle_monitoring).order_by(manifest_oracle_monitoring.file_date.desc()).first()

    # print(str(time_overall.starttime))
    # print(str(time_hive.file_date))
    # print(str(time_oracle.file_date))
    for p in pendings:
        if p.job == "HDFS":
            pending_hdfs.append(p)
        elif p.job == "T0":
            pending_hive.append(p)
    if pending_hdfs:
        time_p_hdfs = pending_hdfs[0].txn_dt
    if pending_hive:
        time_p_hive = pending_hive[0].txn_dt

    query_distinct = Job_Monitoring.query.with_entities(Job_Monitoring.tasklabel).distinct().paginate(page=page, per_page=8)
    next_num = url_for('dashboard_blueprint.dashboard', page=query_distinct.next_num) \
            if query_distinct.has_next else None
    prev_num = url_for('dashboard_blueprint.dashboard', page=query_distinct.prev_num) \
        if query_distinct.has_prev else None

    # print(query_distinct.page)
    # print(query_distinct.per_page)


    return render_template("dashboard.html", query = query_distinct,
                                            running = number_formatter(query_job_running),
                                            query_distinct_count = number_formatter(query_distinct_count),
                                            long_running_count = number_formatter(long_running_count),
                                            next_num=next_num,
                                            prev_num=prev_num,
                                            time_overall=time_overall,
                                            time_lrj=time_lrj,
                                            time_oracle=time_oracle,
                                            time_hive=time_hive,
                                            time_p_hdfs = time_p_hdfs,
                                            time_p_hive = time_p_hive,
                                            pending_hdfs = pending_hdfs,
                                            pending_hive = pending_hive
                                            # pagination =pagination,
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


@dashboard_blueprint.route("/dashboard/<string:status>", methods=['GET', 'POST'])
def status_job(status):
    page = request.args.get('page', 1, type=int)
    query_job_running = Job_Monitoring.query.filter(Job_Monitoring.status == 'RUNNING').count()
    query_distinct_count = Job_Monitoring.query.with_entities(Job_Monitoring.tasklabel).distinct().count()
    long_running_count = Job_Monitoring.query.filter(and_(Job_Monitoring.duration_mins >= 30, Job_Monitoring.status == 'RUNNING')).count()

    # TIME
    time_overall = Job_Monitoring.query.order_by(Job_Monitoring.starttime.desc()).first()
    time_lrj = Job_Monitoring.query.filter(Job_Monitoring.duration_mins >= 30) \
                    .order_by(Job_Monitoring.starttime.desc()).first()
    time_hive = db.session.query(manifest_hive_monitoring).order_by(manifest_hive_monitoring.file_date.desc()).first()
    time_oracle = db.session.query(manifest_oracle_monitoring).order_by(manifest_oracle_monitoring.file_date.desc()).first()

    if status == "RUNNING":
        job_status = Job_Monitoring.query.filter(Job_Monitoring.status == status)\
                                        .order_by(Job_Monitoring.starttime.desc()).paginate(page=page, per_page=8)
    elif status == "TASKS":
        job_status = Job_Monitoring.query.with_entities(Job_Monitoring.tasklabel).distinct().paginate(page=page, per_page=8)


    return render_template('dashboard_status.html', query=job_status,
                                                    status=status,
                                                    running = number_formatter(query_job_running),
                                                    query_distinct_count = number_formatter(query_distinct_count),
                                                    long_running_count = number_formatter(long_running_count),
                                                    time_overall=time_overall,
                                                    time_lrj=time_lrj,
                                                    time_oracle=time_oracle,
                                                    time_hive=time_hive,
                                                    )



# FOR LZERO
@dashboard_blueprint.route('/dashboard_lzero', methods=['GET', 'POST'])
def dashboard_lzero():
    page = request.args.get('page', 1, type=int)
    query_job_running = Job_Monitoring.query.filter(Job_Monitoring.status == 'RUNNING').count()
    query_distinct_count = Job_Monitoring.query.with_entities(Job_Monitoring.tasklabel).distinct().count()
    long_running_count = Job_Monitoring.query.filter(and_(Job_Monitoring.duration_mins >= 30, Job_Monitoring.status == 'RUNNING')).count()
    pendings = db.session.query(pending).all()
    pending_hdfs = []
    time_p_hdfs = None
    pending_hive = []
    time_p_hive = None
    # TIME
    time_overall = Job_Monitoring.query.order_by(Job_Monitoring.starttime.desc()).first()
    time_lrj = Job_Monitoring.query.filter(Job_Monitoring.duration_mins >= 30) \
                    .order_by(Job_Monitoring.starttime.desc()).first()
    time_hive = db.session.query(manifest_hive_monitoring).order_by(manifest_hive_monitoring.file_date.desc()).first()
    time_oracle = db.session.query(manifest_oracle_monitoring).order_by(manifest_oracle_monitoring.file_date.desc()).first()

    # print(str(time_overall.starttime))
    # print(str(time_hive.file_date))
    # print(str(time_oracle.file_date))
    for p in pendings:
        if p.job == "HDFS":
            pending_hdfs.append(p)
        elif p.job == "T0":
            pending_hive.append(p)
    if pending_hdfs:
        time_p_hdfs = pending_hdfs[0].txn_dt
    if pending_hive:
        time_p_hive = pending_hive[0].txn_dt

    query_distinct = Job_Monitoring.query.with_entities(Job_Monitoring.tasklabel).distinct().paginate(page=page, per_page=8)
    next_num = url_for('dashboard_blueprint.dashboard', page=query_distinct.next_num) \
            if query_distinct.has_next else None
    prev_num = url_for('dashboard_blueprint.dashboard', page=query_distinct.prev_num) \
        if query_distinct.has_prev else None

    # print(query_distinct.page)
    # print(query_distinct.per_page)


    return render_template("dashboard_lzero.html", query = query_distinct,
                                            running = number_formatter(query_job_running),
                                            query_distinct_count = number_formatter(query_distinct_count),
                                            long_running_count = number_formatter(long_running_count),
                                            next_num=next_num,
                                            prev_num=prev_num,
                                            time_overall=time_overall,
                                            time_lrj=time_lrj,
                                            time_oracle=time_oracle,
                                            time_hive=time_hive,
                                            time_p_hdfs = time_p_hdfs,
                                            time_p_hive = time_p_hive,
                                            pending_hdfs = pending_hdfs,
                                            pending_hive = pending_hive
                                            # pagination =pagination,
                                            )

@dashboard_blueprint.route("/dashboard_lzero/<string:status>", methods=['GET', 'POST'])
def status_job_lzero(status):
    page = request.args.get('page', 1, type=int)
    query_job_running = Job_Monitoring.query.filter(Job_Monitoring.status == 'RUNNING').count()
    query_distinct_count = Job_Monitoring.query.with_entities(Job_Monitoring.tasklabel).distinct().count()
    long_running_count = Job_Monitoring.query.filter(and_(Job_Monitoring.duration_mins >= 30, Job_Monitoring.status == 'RUNNING')).count()

    # TIME
    time_overall = Job_Monitoring.query.order_by(Job_Monitoring.starttime.desc()).first()
    time_lrj = Job_Monitoring.query.filter(Job_Monitoring.duration_mins >= 30) \
                    .order_by(Job_Monitoring.starttime.desc()).first()
    time_hive = db.session.query(manifest_hive_monitoring).order_by(manifest_hive_monitoring.file_date.desc()).first()
    time_oracle = db.session.query(manifest_oracle_monitoring).order_by(manifest_oracle_monitoring.file_date.desc()).first()

    if status == "RUNNING":
        job_status = Job_Monitoring.query.filter(Job_Monitoring.status == status)\
                                        .order_by(Job_Monitoring.starttime.desc()).paginate(page=page, per_page=8)
    elif status == "TASKS":
        job_status = Job_Monitoring.query.with_entities(Job_Monitoring.tasklabel).distinct().paginate(page=page, per_page=8)


    return render_template('dashboard_status_lzero.html', query=job_status,
                                                    status=status,
                                                    running = number_formatter(query_job_running),
                                                    query_distinct_count = number_formatter(query_distinct_count),
                                                    long_running_count = number_formatter(long_running_count),
                                                    time_overall=time_overall,
                                                    time_lrj=time_lrj,
                                                    time_oracle=time_oracle,
                                                    time_hive=time_hive,
                                                    )