import sys
sys.path.append('../backend')
from flask import Blueprint, request
from jwtctl import generate
from dbctl import DBCTL
import responsesctl as responsesctl
import re


authctl = Blueprint('authctl', __name__)
dbctl = DBCTL()

def get_student_creds(student_code, student_password):
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    result = None
    if cursor:
        sql = '''SELECT CRYPTO_UTIL.DECRYPT(student_code)
        FROM student WHERE CRYPTO_UTIL.DECRYPT(student_code) = :1
        AND CRYPTO_UTIL.DECRYPT(student_password) = :2'''
        fetch = cursor.execute(sql, [student_code, student_password])
        if fetch:
            tmp = fetch.fetchone()
            if tmp:
                result = {'student_code': tmp[0]}  # type: ignore
    dbctl.close_connection()
    return result

def get_admin_creds(admin_code, admin_password):
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    result = None
    if cursor:
        sql = '''SELECT CRYPTO_UTIL.DECRYPT(admin_code)
        FROM admin WHERE CRYPTO_UTIL.DECRYPT(admin_code) = :1
        AND CRYPTO_UTIL.DECRYPT(admin_password) = :2'''
        fetch = cursor.execute(sql, [admin_code, admin_password])
        if fetch:
            tmp = fetch.fetchone()
            if tmp:
                result = {'admin_code': tmp[0]}  # type: ignore
    dbctl.close_connection()
    return result

@authctl.route('/signin', methods=['POST'])
def student_signin():
    data = request.get_json()
    if data:
        student_code = data['student_code'] #* Max length = 9 chars (32 crypto chars)
        student_name = data['student_name'] #* Max length = 40 chars (96 crypto chars)
        student_degree_code = data['student_degree_code'] #* Max length = 4 chars
        student_password = data['student_password'] #* Max length = 25 chars (64 crypto chars)
        if not re.match(r'^[0-9]{9}$', student_code):
            return responsesctl.response(400, 
            message='El codigo de estudiante debe ser igual a 9 caracteres')
        if len(student_name) > 40:
            return responsesctl.response(400, 
            message='El nombre de estudiante debe ser menor a 40 caracteres')
        if len(student_password) > 25:
            return responsesctl.response(400, 
            message='La contraseña debe ser menor a 25 caracteres')
        dbctl.open_connection()
        cursor = dbctl.get_cursor()
        if cursor:
            sql = '''INSERT INTO student 
            VALUES(CRYPTO_UTIL.ENCRYPT(:1), CRYPTO_UTIL.ENCRYPT(:2), CRYPTO_UTIL.ENCRYPT(:3), :4)'''
            cursor.execute(sql, [student_code, student_name, student_password, student_degree_code])
            cursor.connection.commit()
            dbctl.close_connection()
            return responsesctl.response(200, message='Cuenta de usuario creada')
        dbctl.close_connection()
    return responsesctl.response(500, message='Error al crear una cuenta de usuario')

@authctl.route('/login', methods=['POST'])
def student_login():
    data = request.get_json()
    if data:
        creds = get_student_creds(data['student_code'], data['student_password'])
        if creds:
            token = generate({'student_code': creds['student_code'], 'type': 'student'})
            return responsesctl.response(200, token=token)
        return responsesctl.response(404, message='Credenciales incorrectas')
    return responsesctl.response(500, message='Error al iniciar sesion')

@authctl.route('/logout')
def student_logout():
    return ''

@authctl.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if data:
        creds = get_admin_creds(data['admin_code'], data['admin_password'])
        if creds:
            token = generate({'admin_code': data['admin_code'], 'type': 'admin'})
            return responsesctl.response(200, token=token)
        return responsesctl.response(404, message='Credenciales incorrectas')
    return responsesctl.response(500, message='Error al iniciar sesion')
