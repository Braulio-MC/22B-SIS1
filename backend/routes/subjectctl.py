from flask import Blueprint, request
from dbctl import DBContextManager
from responsesctl import response
from jwtctl import token_required
from re import match


subjectctl = Blueprint('subjectctl', __name__)

@subjectctl.route('/subject')
def get_all_subjects():
    with DBContextManager() as cursor:
        output = []
        query = '''SELECT * FROM subject'''
        cursor = cursor.execute(query)
        data = cursor.fetchall()
        for val in data:
            output.append({
                'CVE': val[0],
                'degree_code': val[1],
                'subject_name': val[2],
                'subject_description': val[3],
                'subject_semester': val[4],
                'subject_type': val[5],
                'subject_credits': val[6],
                'last_update_date': val[7]
            })
        return response(200, output)

@subjectctl.route('/subject/<code>')
def get_all_subjects_by_any_code(code):
    code = code.upper()
    column = ''
    if match(r'^I[0-9]{4}$', code):
        column = 'cve'
    elif match(r'^[A-Z]{4}$', code):
        column = 'degree_code'
    else:
        return response(400, message='Codigo invalido')
    with DBContextManager() as cursor:
        output = []
        query = f'''SELECT * FROM subject WHERE {column} = :1'''
        cursor = cursor.execute(query, [code])
        data = cursor.fetchall()
        for val in data:
            output.append({
                'CVE': val[0],
                'degree_code': val[1],
                'subject_name': val[2],
                'subject_description': val[3],
                'subject_semester': val[4],
                'subject_type': val[5],
                'subject_credits': val[6],
                'last_update_date': val[7]
            })
        return response(200, output)

@subjectctl.route('/subject/<degree_code>/<subject_code>')
def get_one_subject(degree_code, subject_code):
    degree_code = degree_code.upper()
    subject_code = subject_code.upper()
    if not match(r'^[A-Z]{4}$', degree_code):
        return response(400, message='Codigo de carrera invalido')
    if not match(r'^I[0-9]{4}$', subject_code):
        return response(400, message='Codigo de materia invalido')
    with DBContextManager() as cursor:
        query = '''SELECT * FROM subject WHERE cve = :1 AND degree_code = :2'''
        cursor = cursor.execute(query, [subject_code, degree_code])
        data = cursor.fetchone()
        if data:
            subject = {
                'CVE': subject_code,
                'degree_code': degree_code,
                'subject_name': data[2],
                'subject_description': data[3],
                'subject_semester': data[4],
                'subject_type': data[5],
                'subject_credits': data[6],
                'last_update_date': data[7]
            }
            return response(200, subject)
        return response(404, message='Materia no encontrada')

@subjectctl.route('/subject', methods=['POST'])
@token_required
def add_subject(current_user):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return response(401, message='Ruta no accesible (administrador inactivo)')
    client_data = request.get_json()
    if client_data:
        cve = client_data['cve']
        degree_code = client_data['degree_code']
        subject_name = client_data['subject_name']
        subject_description = client_data['subject_description']
        subject_semester =  client_data['subject_semester']
        subject_type = client_data['subject_type']
        subject_credits = client_data['subject_credits']
        if not match(r'^I[0-9]{4}$', cve):
            return response(400, message='Codigo de materia invalido')
        if not match(r'^[A-Z]{4}$', degree_code):
            return response(400, message='Codigo de carrera invalido')
        if len(subject_name) > 100:
            return response(400, 
            message='El nombre de materia debe ser menor de 100 caracteres')
        if len(subject_description) > 600:
            return response(400, 
            message='La descripcion de materia debe ser menor de 600 caracteres')
        with DBContextManager() as cursor:
            query = '''INSERT INTO subject VALUES (:1, :2, :3, :4, :5, :6, :7,
            NEW_TIME(SYSDATE, 'GMT', 'CST'))'''
            cursor.execute(query, [cve, degree_code, subject_name, subject_description, 
            subject_semester, subject_type, subject_credits])
            cursor.connection.commit()
            return response(200, message='Materia agregada')
    return response(400, message='Informacion para registrar la materia no encontrada')

@subjectctl.route('/subject/<degree_code>/<subject_code>', methods=['PUT'])
@token_required
def update_subject(current_user, degree_code, subject_code):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return response(401, message='Ruta no accesible (administrador inactivo)')
    degree_code = degree_code.upper()
    subject_code = subject_code.upper()
    if not match(r'^[A-Z]{4}$', degree_code):
        return response(400, message='Codigo de carrera invalido')
    if not match(r'^I[0-9]{4}$', subject_code):
        return response(400, message='Codigo de materia invalido')
    client_data = request.get_json()
    if client_data:
        subject_name = client_data['subject_name']
        subject_description = client_data['subject_description']
        subject_semester =  client_data['subject_semester']
        subject_type = client_data['subject_type']
        subject_credits = client_data['subject_credits']
        if len(subject_name) > 100:
            return response(400, 
            message='El nombre de materia debe ser menor de 100 caracteres')
        if len(subject_description) > 600:
            return response(400, 
            message='La descripcion de materia debe ser menor de 600 caracteres')
        with DBContextManager() as cursor:
            query = '''UPDATE subject SET subject_name = :1, subject_description = :2,
            subject_semester = :3, subject_type = :4, subject_credits = :5,
            last_update_date = NEW_TIME(SYSDATE, 'GMT', 'CST')'''
            cursor.execute(query, [subject_name, subject_description, subject_semester, 
            subject_type, subject_credits])
            cursor.connection.commit()
            return response(200, message='Materia actualizada')
    return response(400, message='Informacion para actualizar la materia no encontrada')
