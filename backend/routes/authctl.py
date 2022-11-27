import sys
sys.path.append('../backend')
from flask import Blueprint, request
from jwtctl import generate
from dbctl import DBContextManager
from responsesctl import response
from re import match


authctl = Blueprint('authctl', __name__)

def get_student_creds(student_code, student_password):
    result = None
    with DBContextManager() as cursor:
        query = '''SELECT CRYPTO_UTIL.DECRYPT(student_code)
        FROM student WHERE CRYPTO_UTIL.DECRYPT(student_code) = :1
        AND CRYPTO_UTIL.DECRYPT(student_password) = :2'''
        cursor = cursor.execute(query, [student_code, student_password])
        data = cursor.fetchone()
        if data:
            result = {'student_code': data[0]}
    return result

@authctl.route('/signin', methods=['POST'])
def student_signin():
    client_data = request.get_json()
    if client_data:
        student_code = client_data['student_code']
        student_name = client_data['student_name']
        student_degree_code = client_data['student_degree_code']
        student_password = client_data['student_password']
        if not match(r'^[0-9]{9}$', student_code):
            return response(400, 
            message='El codigo de estudiante debe ser igual a 9 caracteres numericos')
        if len(student_name) > 40:
            return response(400, 
            message='El nombre de estudiante debe ser menor a 40 caracteres')
        if len(student_password) > 25:
            return response(400, 
            message='La contraseña debe ser menor a 25 caracteres')
        with DBContextManager() as cursor:
            query = '''INSERT INTO student 
            VALUES(CRYPTO_UTIL.ENCRYPT(:1), CRYPTO_UTIL.ENCRYPT(:2), 
            CRYPTO_UTIL.ENCRYPT(:3), :4)'''
            cursor.execute(query, [student_code, student_name, 
            student_password, student_degree_code])
            cursor.connection.commit()
            return response(200, message='Cuenta de usuario creada')
    return response(400, message='Informacion para crear un usuario no encontrada')

@authctl.route('/login', methods=['POST'])
def student_login():
    data = request.get_json()
    if data:
        creds = get_student_creds(data['student_code'], data['student_password'])
        if creds:
            token = generate({'student_code': creds['student_code'], 'type': 'student'})
            return response(200, token=token)
        return response(404, message='Credenciales incorrectas')
    return response(400, message='Informacion para iniciar sesion no encontrada')

@authctl.route('/logout')
def student_logout():
    return ''
 