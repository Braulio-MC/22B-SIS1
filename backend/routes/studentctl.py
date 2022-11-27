from flask import Blueprint, request
from jwtctl import token_required
from dbctl import DBContextManager
from responsesctl import response
from re import match


studentctl = Blueprint('studentctl', __name__)

@studentctl.route('/student/user-info')
@token_required
def get_current_student(current_user):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'student':
        return response(401, message='Inicia sesion como estudiante')
    return response(200, **current_user)

@studentctl.route('/student')
@token_required
def get_all_students(current_user):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return response(401, message='Ruta no accesible (administrador inactivo)')
    with DBContextManager() as cursor:
        output = []
        query = '''SELECT CRYPTO_UTIL.DECRYPT(student.student_code),
        CRYPTO_UTIL.DECRYPT(student.student_name), 
        student.degree_code, degree.degree_name, student.creation_date FROM student 
        INNER JOIN degree ON student.degree_code = degree.degree_code'''
        cursor = cursor.execute(query)
        data = cursor.fetchall()
        for val in data:
            output.append({
                'student_code': val[0],
                'student_name': val[1],
                'degree_code': val[2],
                'degree_name': val[3],
                'creation_date': val[4],
                'type': 'student'
            })
        return response(200, output)

@studentctl.route('/student/<student_code>')
@token_required
def get_one_student(current_user, student_code):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return response(401, message='Ruta no accesible (administrador inactivo)')
    if not match(r'^[0-9]{9}$', student_code):
        return response(400, message='Codigo de estudiante invalido')
    with DBContextManager() as cursor:
        query = '''SELECT CRYPTO_UTIL.DECRYPT(student.student_name), 
        student.degree_code, degree.degree_name, student.creation_date FROM student 
        INNER JOIN degree ON student.degree_code = degree.degree_code
        WHERE CRYPTO_UTIL.DECRYPT(student.student_code) = :1'''
        cursor = cursor.execute(query, [student_code])
        data = cursor.fetchone()
        if data:
            student = {
                'student_code': student_code,
                'student_name': data[0],  
                'degree_code': data[1],  
                'degree_name': data[2],  
                'creation_date': data[3],  
                'type': 'student'
            }
            return response(200, student)
        return response(404, message='No existe estudiante con el codigo proporcionado')

@studentctl.route('/student', methods=['PUT'])
@token_required
def update_student(current_user):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'student':
        return response(401, message='Inicia sesion como estudiante')
    client_data = request.get_json()
    if client_data:
        student_code = current_user['student_code']
        student_name = client_data['student_name']
        student_password = client_data['student_password']
        if len(student_name) > 40:
            return response(400, 
            message='El nombre de estudiante debe ser menor a 40 caracteres')
        if len(student_password) > 25:
            return response(400, 
            message='La contraseña debe ser menor a 25 caracteres')
        with DBContextManager() as cursor:
            query = '''UPDATE student SET student_name = CRYPTO_UTIL.ENCRYPT(:1),
            student_password = CRYPTO_UTIL.ENCRYPT(:2) 
            WHERE CRYPTO_UTIL.DECRYPT(student_code) = :3'''
            cursor.execute(query, [student_name, student_password, student_code])
            cursor.connection.commit()
            return response(200, message='Cuenta de usuario actualizada')
    return response(400, message='Informacion para actualizar al estudiante no encontrada')

@studentctl.route('/student', methods=['POST'])
@token_required
def insert_student(current_user):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return response(401, message='Ruta no accesible (administrador inactivo)')
    client_data = request.get_json()
    if client_data:
        student_code = client_data['student_code']
        student_name = client_data['student_name']
        student_password = client_data['student_password']
        student_degree_code = client_data['student_degree_code']
        student_degree_code = student_degree_code.upper()
        if not match(r'^[0-9]{9}$', student_code):
            return response(400, 
            message='El codigo de estudiante debe ser igual a 9 caracteres numericos')
        if len(student_name) > 40:
            return response(400, 
            message='El nombre de estudiante debe ser menor a 40 caracteres')
        if len(student_password) > 25:
            return response(400, 
            message='La contraseña debe ser menor a 25 caracteres')
        if not match(r'^[A-Z]{4}$', student_degree_code):
            return response(400, message='Codigo de carrera invalido')
        with DBContextManager() as cursor:
            query = '''INSERT INTO student VALUES(CRYPTO_UTIL.ENCRYPT(:1), 
            CRYPTO_UTIL.ENCRYPT(:2), CRYPTO_UTIL.ENCRYPT(:3), :4)'''
            cursor.execute(query, [student_code, student_name, 
            student_password, student_degree_code])
            cursor.connection.commit()
            return response(200, message='Cuenta de usuario creada')
    return response(400, message='Informacion para crear al estudiante no encontrada')
