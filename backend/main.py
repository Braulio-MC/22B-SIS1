"""
? DB time zone: UTC/GMT -7 hours(current offset)/San Jose, CA.
"""

from flask import Flask
from routes.authctl import authctl
from routes.degreectl import degreectl
from routes.modularctl import modularctl
from routes.servicectl import servicectl
from routes.subjectctl import subjectctl
from routes.studentctl import studentctl
from routes.adminctl import adminctl


app = Flask(__name__)
app.register_blueprint(authctl)
app.register_blueprint(degreectl)
app.register_blueprint(modularctl)
app.register_blueprint(servicectl)
app.register_blueprint(subjectctl)
app.register_blueprint(studentctl)
app.register_blueprint(adminctl)
