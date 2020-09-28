from flask import render_template, request, url_for, jsonify, Response, Blueprint
from smartdashboard.models import Job_BCA
from sqlalchemy import and_
from smartdashboard import db, bca_monitoring_table
from datetime import date, datetime
from smartdashboard.utils import time_to_seconds
from dateutil.relativedelta import relativedelta

others_blueprint = Blueprint('others_blueprint', __name__)

@others_blueprint.route('/error-404')
def error_404():
    return render_template('error-404.html')

@others_blueprint.route('/error-500')
def error_500():
    return render_template('error-500.html')

@others_blueprint.route('/login')
def login():
    return render_template('login.html')

@others_blueprint.route('/register')
def register():
    return render_template('register.html')

@others_blueprint.route('/blank-page')
def blank_page():
    return render_template('blank-page.html')