from flask import Blueprint
from jwtctl import token_required
from dbctl import DBCTL
import responsesctl

adminctl = Blueprint('adminctl', __name__)
dbctl = DBCTL()

@adminctl.route('/admin/current')
@token_required
def get_current_admin(current_user):
    if not current_user:
        return responsesctl.response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return responsesctl.response(401, message='Ruta no accesible')
    return responsesctl.response(200, **current_user)