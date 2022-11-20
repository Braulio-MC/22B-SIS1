from flask import Blueprint, request
from dbctl import DBCTL
import responsesctl
from jwtctl import token_required
import re

servicectl = Blueprint('servicectl', __name__)
dbctl = DBCTL()

@servicectl.route('/social-service')
def get_all_social_services():
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    output = []
    if cursor:
        sql = '''SELECT * FROM social_service'''
        fetch = cursor.execute(sql)
        if fetch:
            tmp = fetch.fetchall()
            dbctl.close_connection()
            for val in tmp:
                output.append({
                    'social_service_code': val[0],  
                    'social_service_name': val[1],  
                    'social_service_description': val[2],  
                    'last_update_date': val[3]  
                })
            return responsesctl.response(200, output)
    dbctl.close_connection()
    return responsesctl.response(500, message='Error al obtener informacion del servicio social')

@servicectl.route('/social-service/<service_code>')
def get_one_social_service(service_code):
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    if cursor:
        sql = '''SELECT * FROM social_service WHERE social_service_code = :1'''
        fetch = cursor.execute(sql, [service_code])
        if fetch:
            tmp = fetch.fetchone()
            dbctl.close_connection()
            if tmp:
                ss = {
                    'social_service_code': tmp[0],  # type: ignore
                    'social_service_name': tmp[1],  # type: ignore
                    'social_service_description': tmp[2],  # type: ignore
                    'last_update_date': tmp[3]  # type: ignore
                }
                return responsesctl.response(200, ss)
            return responsesctl.response(404, message='Servicio social no disponible')
    dbctl.close_connection()
    return responsesctl.response(500, message='Error al obtener informacion del servicio social')

@servicectl.route('/social-service', methods=['POST'])
@token_required
def insert_social_service(current_user):
    if not current_user:
        return responsesctl.response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return responsesctl.response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return responsesctl.response(401, message='Ruta no accesible (administrador inactivo)')
    data = request.get_json()
    if data:
        social_service_name = data['social_service_name'] #* Max length = 20 chars
        social_service_description = data['social_service_description'] #* Max length = 1500 chars
        if len(social_service_name) > 20:
            return responsesctl.response(400, 
            message='El nombre del servicio social debe ser menor a 20 caracteres')
        if len(social_service_description) > 1500:
            return responsesctl.response(400, 
            message='La descripcion para el servicio social debe ser menor de 1500 caracteres')
        dbctl.open_connection()
        cursor = dbctl.get_cursor()
        if cursor:
            sql = '''INSERT INTO social_service VALUES (seq_social_service.nextval, 
            :1, :2, NEW_TIME(SYSDATE, 'GMT', 'CST'))'''
            cursor.execute(sql, [social_service_name, social_service_description])
            cursor.connection.commit()
            dbctl.close_connection()
            return responsesctl.response(200, message='Servicio social agregado')
        dbctl.close_connection()
    return responsesctl.response(500, message='Error al agregar un nuevo servicio social')

@servicectl.route('/social-service/<service_code>', methods=['PUT'])
@token_required
def update_social_service(current_user, service_code):
    if not current_user:
        return responsesctl.response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return responsesctl.response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return responsesctl.response(401, message='Ruta no accesible (administrador inactivo)')
    if not re.match(r'^[0-9]{1}$', service_code):
        return responsesctl.response(400, message='Codigo de servicio social invalido')
    data = request.get_json()
    if data:
        social_service_name = data['social_service_name'] #* Max length = 20 chars
        social_service_description = data['social_service_description'] #* Max length = 1500 chars
        if len(social_service_name) > 20:
            return responsesctl.response(400, 
            message='El nombre del servicio social debe ser menor a 20 caracteres')
        if len(social_service_description) > 1500:
            return responsesctl.response(400, 
            message='La descripcion para el servicio social debe ser menor de 1500 caracteres')
        dbctl.open_connection()
        cursor = dbctl.get_cursor()
        if cursor:
            sql = '''UPDATE social_service SET social_service_name = :1, 
            social_service_description = :2, last_update_date = NEW_TIME(SYSDATE, 'GMT', 'CST') 
            WHERE social_service_code = :3'''
            cursor.execute(sql, [social_service_name, social_service_description, service_code])
            cursor.connection.commit()
            dbctl.close_connection()
            return responsesctl.response(200, message='Servicio social actualizado')
        dbctl.close_connection()
    return responsesctl.response(500, message='Error al actualizar el servicio social')
