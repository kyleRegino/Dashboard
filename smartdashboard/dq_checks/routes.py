from flask import render_template, request, url_for, jsonify, Response, Blueprint
from smartdashboard import session, manifest_hive_monitoring, manifest_oracle_monitoring
from smartdashboard.utils import init_list

from sqlalchemy import or_, and_
from sqlalchemy.sql import func

from datetime import date

dq_blueprint = Blueprint('dq_blueprint', __name__)

# MANIFEST VS HIVE
@dq_blueprint.route('/dq_manvshive')
def dq_manvshive():

    variance_com = session.query(func.sum(manifest_hive_monitoring.variance)).filter(and_(manifest_hive_monitoring.cdr_type =="com",manifest_hive_monitoring.file_date == date.today())).scalar()
    variance_vou = session.query(func.sum(manifest_hive_monitoring.variance)).filter(and_(manifest_hive_monitoring.cdr_type =="vou",manifest_hive_monitoring.file_date == date.today())).scalar()
    variance_first = session.query(func.sum(manifest_hive_monitoring.variance)).filter(and_(manifest_hive_monitoring.cdr_type =="first",manifest_hive_monitoring.file_date == date.today())).scalar()
    variance_mon = session.query(func.sum(manifest_hive_monitoring.variance)).filter(and_(manifest_hive_monitoring.cdr_type =="mon",manifest_hive_monitoring.file_date == date.today())).scalar()
    variance_cm = session.query(func.sum(manifest_hive_monitoring.variance)).filter(and_(manifest_hive_monitoring.cdr_type =="cm",manifest_hive_monitoring.file_date == date.today())).scalar()
    variance_adj = session.query(func.sum(manifest_hive_monitoring.variance)).filter(and_(manifest_hive_monitoring.cdr_type =="adj",manifest_hive_monitoring.file_date == date.today())).scalar()

    return render_template('dqchecks_manvshive.html', variance_com = variance_com,
                                                variance_vou = variance_vou,
                                                variance_first = variance_first,
                                                variance_mon = variance_mon,
                                                variance_cm = variance_cm,
                                                variance_adj = variance_adj)

@dq_blueprint.route('/dqchecks_manvshive_js', methods=['GET','POST'])
def dqchecks_manvshive_js():
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

@dq_blueprint.route('/dqchecks_manvshive_search', methods=['POST'])
def dqchecks_manvshive_search():
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

# MANIFEST VS ORACLE
@dq_blueprint.route('/dq_manvsoracle', methods=['GET', 'POST'])
def dq_manvsoracle():
    variance_com = session.query(func.sum(manifest_oracle_monitoring.variance)).filter(and_(manifest_oracle_monitoring.cdr_type =="com",manifest_oracle_monitoring.file_date == date.today())).scalar()
    variance_vou = session.query(func.sum(manifest_oracle_monitoring.variance)).filter(and_(manifest_oracle_monitoring.cdr_type =="vou",manifest_oracle_monitoring.file_date == date.today())).scalar()
    variance_first = session.query(func.sum(manifest_oracle_monitoring.variance)).filter(and_(manifest_oracle_monitoring.cdr_type =="first",manifest_oracle_monitoring.file_date == date.today())).scalar()
    variance_mon = session.query(func.sum(manifest_oracle_monitoring.variance)).filter(and_(manifest_oracle_monitoring.cdr_type =="mon",manifest_oracle_monitoring.file_date == date.today())).scalar()
    variance_cm = session.query(func.sum(manifest_oracle_monitoring.variance)).filter(and_(manifest_oracle_monitoring.cdr_type =="cm",manifest_oracle_monitoring.file_date == date.today())).scalar()
    variance_adj = session.query(func.sum(manifest_oracle_monitoring.variance)).filter(and_(manifest_oracle_monitoring.cdr_type =="adj",manifest_oracle_monitoring.file_date == date.today())).scalar()

    return render_template('dqchecks_manvsoracle.html', variance_com = variance_com,
                                                variance_vou = variance_vou,
                                                variance_first = variance_first,
                                                variance_mon = variance_mon,
                                                variance_cm = variance_cm,
                                                variance_adj = variance_adj
                                                )

@dq_blueprint.route('/dqchecks_manvsoracle_js', methods=['GET','POST'])
def dqchecks_manvsoracle_js():
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

@dq_blueprint.route('/dqchecks_manvsoracle_search', methods=['POST'])
def dqchecks_manvsoracle_search():
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
