from flask import Flask
from flask_cors import CORS
from routes.authctl import authctl
from routes.degreectl import degreectl
from routes.modularctl import modularctl
from routes.servicectl import servicectl
from routes.subjectctl import subjectctl
from routes.studentctl import studentctl
from routes.adminctl import adminctl
from routes.modularcommentsctl import modularcommentsctl
from routes.servicecommentsctl import servicecommentsctl
from routes.subjectcommentsctl import subjectcommentsctl


app = Flask(__name__)
CORS(app)
app.register_blueprint(authctl)
app.register_blueprint(degreectl)
app.register_blueprint(modularctl)
app.register_blueprint(servicectl)
app.register_blueprint(subjectctl)
app.register_blueprint(studentctl)
app.register_blueprint(adminctl)
app.register_blueprint(modularcommentsctl)
app.register_blueprint(servicecommentsctl)
app.register_blueprint(subjectcommentsctl)
