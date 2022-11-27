from flask import Blueprint, request
from jwtctl import token_required
from dbctl import DBContextManager
from responsesctl import response
from re import match


modularctl = Blueprint('modularctl', __name__)

@modularctl.route('/modular')
def get_all_modulars():
    with DBContextManager() as cursor:
        output = []
        query = '''SELECT * FROM modular_project'''
        cursor = cursor.execute(query)
        data = cursor.fetchall()
        for val in data:
            output.append({
                'modular_project_code': val[0],
                'degree_code': val[1],
                'modular_project_description': val[2],
                'last_update_date': val[3]
            })
        return response(200, output)

@modularctl.route('/modular/<modular_code>')
def get_one_modular(modular_code):
    modular_code = modular_code.upper()
    if not match(r'^[A-Z]{7}$', modular_code):
        return response(400, message='Codigo de proyecto modular invalido')
    with DBContextManager() as cursor:
        query = '''SELECT * FROM modular_project WHERE modular_project_code = :1'''
        cursor = cursor.execute(query, [modular_code])
        data = cursor.fetchone()
        if data:
            modular = {
                'modular_project_code': data[0],
                'degree_code': data[1],
                'modular_project_description': data[2],
                'last_update_date': data[3]
            }
            return response(200, modular)
        return response(404, message='Proyecto modular no encontrado')

@modularctl.route('/modular', methods=['POST'])
@token_required
def insert_modular(current_user):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return response(401, message='Ruta no accesible (administrador inactivo)')
    client_data = request.get_json()
    if client_data:
        degree_code = client_data['degree_code']
        degree_code = degree_code.upper()
        modular_project_description = client_data['modular_project_description']
        if not match(r'^[A-Z]{4}$', degree_code):
            return response(400, message='Codigo de carrera invalido')
        if len(modular_project_description) > 1500:
            return response(400, 
            message='La descripcion del proyecto modular debe ser menor de 1500 caracteres')
        modular_project_code = f'MOD{degree_code}'
        with DBContextManager() as cursor:
            query = '''INSERT INTO modular_project VALUES (:1, :2, :3, 
            NEW_TIME(SYSDATE, 'GMT', 'CST'))'''
            cursor.execute(query, [modular_project_code, degree_code, modular_project_description])
            cursor.connection.commit()
            return response(200, 
            message=f'Proyecto modular agregado: {modular_project_code}')
    return response(400, message='Informacion para agregar el proyecto modular no encontrada')

@modularctl.route('/modular/<modular_code>', methods=['PUT'])
@token_required
def update_modular(current_user, modular_code):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return response(401, message='Ruta no accesible (administrador inactivo)')
    modular_code = modular_code.upper()
    if not match(r'^[A-Z]{7}$', modular_code):
        return response(400, message='Codigo de proyecto modular invalido')
    client_data = request.get_json()
    if client_data:
        modular_project_description = client_data['modular_project_description']
        if len(modular_project_description) > 1500:
            return response(400, 
            message='La descripcion del proyecto modular debe ser menor de 1500 caracteres')
        with DBContextManager() as cursor:
            query = '''UPDATE modular_project SET modular_project_description = :1,
            last_update_date = NEW_TIME(SYSDATE, 'GMT', 'CST') 
            WHERE modular_project_code = :2'''
            cursor.execute(query, [modular_project_description, modular_code])
            cursor.connection.commit()
            return response(200, message='Proyecto modular actualizado')
    return response(500, message='Informacion para actualizar el proyecto modular no encontrada')
