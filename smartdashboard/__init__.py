
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://talendmgmt:aA_1234567890*@10.126.10.238:3306/talend_mgmt'
# app.config['SQLALCHEMY_BINDS'] = { 'db1': 'oracle://talend_user:talend12345#@10.123.94.31:1521/BIODS'}

# Renzo Configs
Base = automap_base()
# engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

db = SQLAlchemy(app)
Base.prepare(db.engine, reflect=True)

bca_monitoring_table = Base.classes.job_bca_monitoring


session = Session(db.engine)

from smartdashboard import routes