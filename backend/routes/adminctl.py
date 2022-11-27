from flask import Blueprint, request
from jwtctl import token_required
from responsesctl import response
from dbctl import DBContextManager
from jwtctl import generate


adminctl = Blueprint('adminctl', __name__)

def get_admin_creds(admin_code, admin_password):
    result = None
    with DBContextManager() as cursor:
        query = '''SELECT CRYPTO_UTIL.DECRYPT(admin_code)
        FROM admin WHERE CRYPTO_UTIL.DECRYPT(admin_code) = :1
        AND CRYPTO_UTIL.DECRYPT(admin_password) = :2'''
        cursor = cursor.execute(query, [admin_code, admin_password])
        data = cursor.fetchone()
        if data:
            result = {'admin_code': data[0]}
    return result

@adminctl.route('/admin/user-info')
@token_required
def get_current_admin(current_user):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return response(401, message='Ruta no accesible (administrador inactivo)')
    return response(200, **current_user)

@adminctl.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if data:
        creds = get_admin_creds(data['admin_code'], data['admin_password'])
        if creds:
            token = generate({'admin_code': data['admin_code'], 'type': 'admin'})
            return response(200, token=token)
        return response(404, message='Credenciales incorrectas')
    return response(400, message='Informacion para inicio de sesion no encontrada')