from flask import Blueprint, request
from dbctl import DBContextManager
from responsesctl import response
from jwtctl import token_required
from re import match


servicectl = Blueprint('servicectl', __name__)

@servicectl.route('/social-service')
def get_all_social_services():
    with DBContextManager() as cursor:
        output = []
        query = '''SELECT * FROM social_service'''
        cursor = cursor.execute(query)
        data = cursor.fetchall()
        for val in data:
            output.append({
                'social_service_code': val[0],  
                'social_service_name': val[1],  
                'social_service_description': val[2],  
                'last_update_date': val[3]  
            })
        return response(200, output)

@servicectl.route('/social-service/<service_code>')
def get_one_social_service(service_code):
    if not match(r'^[0-9]{1,}$', service_code):
        return response(400, message='Codigo de servicio invalido')
    with DBContextManager() as cursor:
        query = '''SELECT * FROM social_service WHERE social_service_code = :1'''
        cursor = cursor.execute(query, [service_code])
        data = cursor.fetchone()
        if data:
            ss = {
                'social_service_code': data[0],  
                'social_service_name': data[1],  
                'social_service_description': data[2],  
                'last_update_date': data[3]  
            }
            return response(200, ss)
        return response(404, message='Servicio social no disponible')

@servicectl.route('/social-service', methods=['POST'])
@token_required
def insert_social_service(current_user):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return response(401, message='Ruta no accesible (administrador inactivo)')
    client_data = request.get_json()
    if client_data:
        social_service_name = client_data['social_service_name']
        social_service_description = client_data['social_service_description']
        if len(social_service_name) > 20:
            return response(400, 
            message='El nombre del servicio social debe ser menor a 20 caracteres')
        if len(social_service_description) > 1500:
            return response(400, 
            message='La descripcion para el servicio social debe ser menor de 1500 caracteres')
        with DBContextManager() as cursor:
            query = '''INSERT INTO social_service VALUES (seq_social_service.nextval, 
            :1, :2, NEW_TIME(SYSDATE, 'GMT', 'CST'))'''
            cursor.execute(query, [social_service_name, social_service_description])
            cursor.connection.commit()
            return response(200, message='Servicio social agregado')
    return response(400, message='Informacion para agregar el servicio no encontrada')

@servicectl.route('/social-service/<service_code>', methods=['PUT'])
@token_required
def update_social_service(current_user, service_code):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return response(401, message='Ruta no accesible (administrador inactivo)')
    if not match(r'^[0-9]{1,}$', service_code):
        return response(400, message='Codigo de servicio invalido')
    client_data = request.get_json()
    if client_data:
        social_service_name = client_data['social_service_name']
        social_service_description = client_data['social_service_description']
        if len(social_service_name) > 20:
            return response(400, 
            message='El nombre del servicio social debe ser menor a 20 caracteres')
        if len(social_service_description) > 1500:
            return response(400, 
            message='La descripcion para el servicio social debe ser menor de 1500 caracteres')
        with DBContextManager() as cursor:
            query = '''UPDATE social_service SET social_service_name = :1, 
            social_service_description = :2, last_update_date = NEW_TIME(SYSDATE, 'GMT', 'CST') 
            WHERE social_service_code = :3'''
            cursor.execute(query, [social_service_name, social_service_description, service_code])
            cursor.connection.commit()
            return response(200, message='Servicio social actualizado')
    return response(400, message='Informacion para actualizar el servicio no encontrada')
