from flask import Blueprint, request
from dbctl import DBContextManager
from jwtctl import token_required
from responsesctl import response
from re import match


degreectl = Blueprint('degreectl', __name__)

def check_for_degree(degree_code):
    with DBContextManager() as cursor:
        query = '''SELECT degree_code FROM degree WHERE degree_code = :1'''
        cursor = cursor.execute(query, [degree_code])
        data = cursor.fetchone()
        if data:
            return data[0]
    return None

@degreectl.route('/degree')
def get_all_degrees():
    with DBContextManager() as cursor:
        output = []
        query = '''SELECT * FROM degree'''
        cursor = cursor.execute(query)
        data = cursor.fetchall()
        for val in data:
            output.append({
                'degree_code': val[0],
                'degree_name': val[1],
                'degree_description': val[2],
                'no_subjects': val[3],
                'no_semesters': val[4],
                'last_update_date': val[5]
            })
        return response(200, output)

@degreectl.route('/degree/<degree_code>')
def get_one_degree(degree_code):
    degree_code = degree_code.upper()
    if not match(r'^[A-Z]{4}$', degree_code):
        return response(400, message='Codigo de carrera invalido')
    with DBContextManager() as cursor:
        query = '''SELECT * FROM degree WHERE degree_code = :1'''
        cursor = cursor.execute(query, [degree_code])
        data = cursor.fetchone()
        if data:
            subject = {
                'degree_code': data[0],
                'degree_name': data[1],
                'degree_description': data[2],
                'no_subjects': data[3],
                'no_semesters': data[4],
                'last_update_date': data[5]
            }
            return response(200, subject)
        return response(404, message='Carrera no encontrada')

@degreectl.route('/degree', methods=['POST'])
@token_required
def insert_degree(current_user):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return response(401, message='Ruta no accesible (administrador inactivo)')
    client_data = request.get_json()
    if client_data:
        degree_code = client_data['degree_code']
        degree_name = client_data['degree_name']
        degree_description = client_data['degree_description'] 
        no_subjects = client_data['no_subjects']
        no_semesters = client_data['no_semesters']
        degree_code = degree_code.upper()
        if not match(r'^[A-Z]{4}$', degree_code):
            return response(400, message='Codigo de carrera invalido')
        if len(degree_name) > 60:
            return response(400,
            message='El nombre de carrera debe ser menor a 60 caracteres')
        if len(degree_description) > 900:
            return response(400, 
            message='La descripcion de carrera debe ser menor a 900 caracteres')
        with DBContextManager() as cursor:
            query = '''INSERT INTO degree VALUES (:1, :2, :3, :4, :5, 
            NEW_TIME(SYSDATE, 'GMT', 'CST'))'''
            cursor.execute(query, [degree_code, degree_name, degree_description, 
            no_subjects, no_semesters])
            cursor.connection.commit()
            return response(200, message='Carrera agregada')
    return response(400, message='Informacion para agregar la carrera no encontrada')

@degreectl.route('/degree/<degree_code>', methods=['PUT'])
@token_required
def update_degree(current_user, degree_code):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return response(401, message='Ruta no accesible (administrador inactivo)')
    degree_code = degree_code.upper()
    if not match(r'^[A-Z]{4}$', degree_code):
        return response(400, message='Codigo de carrera invalido')
    if not check_for_degree(degree_code):
        return response(404, message='Carrera no encontrada') 
    client_data = request.get_json()
    if client_data:
        degree_name = client_data['degree_name']
        degree_description = client_data['degree_description']
        no_subjects = client_data['no_subjects'] 
        no_semesters = client_data['no_semesters']
        if len(degree_name) > 60:
            return response(400,
            message='El nombre de carrera debe ser menor a 60 caracteres')
        if len(degree_description) > 900:
            return response(400, 
            message='La descripcion de carrera debe ser menor a 900 caracteres')
        with DBContextManager() as cursor:
            query = '''UPDATE degree SET degree_name = :1, degree_description = :2, 
            no_subjects = :3, no_semesters = :4, 
            last_update_date = NEW_TIME(SYSDATE, 'GMT', 'CST') WHERE degree_code = :5'''
            cursor.execute(query, [degree_name, degree_description, no_subjects, 
            no_semesters, degree_code])
            cursor.connection.commit()
            return response(200, message='Carrera actualizada')
    return response(400, message='Informacion para actualizar la carrera no encontrada')
