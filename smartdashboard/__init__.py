
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
db.init_app(app)
Base.prepare(db.engine, reflect=True)

bca_monitoring_table = Base.classes.job_bca_monitoring
manifest_hive_monitoring = Base.classes.manifest_hive_monitoring
manifest_oracle_monitoring = Base.classes.manifest_oracle_monitoring
top_sku_talendfc = Base.classes.top_sku_talendfc
cdr_threshold = Base.classes.cdr_threshold


session = Session(db.engine)

# from smartdashboard import routes

from smartdashboard.dashboard.routes import dashboard_blueprint
from smartdashboard.long_running_jobs.routes import lrj_blueprint
from smartdashboard.bca_monitoring.routes import bca_blueprint
from smartdashboard.dq_checks.routes import dq_blueprint
from smartdashboard.topsku.routes import topsku_blueprint

app.register_blueprint(dashboard_blueprint)
app.register_blueprint(lrj_blueprint)
app.register_blueprint(bca_blueprint)
app.register_blueprint(dq_blueprint)
app.register_blueprint(topsku_blueprint)