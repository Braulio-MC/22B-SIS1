from flask import Blueprint, request
from jwtctl import token_required
from dbctl import DBCTL
import responsesctl


studentctl = Blueprint('studentctl', __name__)
dbctl = DBCTL()

@studentctl.route('/student/current')
@token_required
def get_current_student(current_user):
    if not current_user:
        return responsesctl.response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'student':
        return responsesctl.response(401, message='Inicia sesion como estudiante')
    return responsesctl.response(200, **current_user)

@studentctl.route('/student')
@token_required
def get_all_students(current_user):
    if not current_user:
        return responsesctl.response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return responsesctl.response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return responsesctl.response(401, message='Ruta no accesible (administrador inactivo)')
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    output = []
    if cursor:
        sql = '''SELECT CRYPTO_UTIL.DECRYPT(student.student_code),
        CRYPTO_UTIL.DECRYPT(student.student_name), 
        student.degree_code, degree.degree_name, student.creation_date FROM ADMIN.student 
        INNER JOIN ADMIN.degree ON student.degree_code = degree.degree_code'''
        fetch = cursor.execute(sql)
        if fetch:
            tmp = fetch.fetchall()
            dbctl.close_connection()
            if tmp:
                for s in tmp:
                    output.append({
                        'student_code': s[0],
                        'student_name': s[1],
                        'degree_code': s[2],
                        'degree_name': s[3],
                        'creation_date': s[4],
                        'type': 'student'
                    })
                return responsesctl.response(200, output)
    dbctl.close_connection()
    return responsesctl.response(500, message='Error al obtener informacion de estudiantes')

@studentctl.route('/student/<student_code>')
@token_required
def get_one_student(current_user, student_code):
    if not current_user:
        return responsesctl.response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return responsesctl.response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return responsesctl.response(401, message='Ruta no accesible (administrador inactivo)')
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    if cursor:
        sql = '''SELECT CRYPTO_UTIL.DECRYPT(student.student_name), 
        student.degree_code, degree.degree_name, student.creation_date FROM ADMIN.student 
        INNER JOIN ADMIN.degree ON student.degree_code = degree.degree_code
        WHERE CRYPTO_UTIL.DECRYPT(student.student_code) = :1'''
        fetch = cursor.execute(sql, [student_code])
        if fetch:
            tmp = fetch.fetchone()
            dbctl.close_connection()
            if tmp:
                student = {
                    'student_code': student_code,
                    'student_name': tmp[0],  # type: ignore
                    'degree_code': tmp[1],  # type: ignore
                    'degree_name': tmp[2],  # type: ignore
                    'creation_date': tmp[3],  # type: ignore
                    'type': 'student'
                }
                return responsesctl.response(200, student)
    dbctl.close_connection()
    return responsesctl.response(500, message='Error al obtener informacion del estudiante')

#? type admin can also perform an alter student
@studentctl.route('/student/<student_code>', methods=['PUT'])
@token_required
def alter_student(current_user, student_code):
    if not current_user:
        return responsesctl.response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'student':
        return responsesctl.response(401, message='Inicia sesion como estudiante')
    data = request.get_json()
    if data:
        if len(data['student_name']) > 40:
            return responsesctl.response(400, 
            message='El nombre de estudiante debe ser menor a 40 caracteres')
        if len(data['student_password']) > 25:
            return responsesctl.response(400, 
            message='La contraseña debe ser menor a 25 caracteres') 
        dbctl.open_connection()
        cursor = dbctl.get_cursor()
        if cursor:
            sql = '''UPDATE student SET student_name = CRYPTO_UTIL.ENCRYPT(:1),
            student_password = CRYPTO_UTIL.ENCRYPT(:2) 
            WHERE CRYPTO_UTIL.DECRYPT(student_code) = :3'''
            cursor.execute(sql, [data['student_name'], data['student_password'], student_code])
            cursor.connection.commit()
            dbctl.close_connection()
            return responsesctl.response(200, message='Cuenta de usuario modificada')
        dbctl.close_connection()
    return responsesctl.response(500, message='Error al modificar la cuenta de usuario')

#? INSERT