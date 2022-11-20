from flask import Blueprint, request
from jwtctl import token_required
from dbctl import DBCTL
import responsesctl
import re


modularctl = Blueprint('modularctl', __name__)
dbctl = DBCTL()

@modularctl.route('/modular')
def get_all_modulars():
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    output = []
    if cursor:
        sql = '''SELECT * FROM modular_project'''
        fetch = cursor.execute(sql)
        if fetch:
            tmp = fetch.fetchall()
            dbctl.close_connection()
            for val in tmp:
                output.append({
                    'modular_project_code': val[0],
                    'degree_code': val[1],
                    'modular_project_description': val[2],
                    'last_update_date': val[3]
                })
            return responsesctl.response(200, output)
    dbctl.close_connection()
    return responsesctl.response(500, 
    message='Error al obtener informacion de los proyectos modulares')

@modularctl.route('/modular/<modular_code>')
def get_one_modular(modular_code):
    if not re.match(r'^[a-z]{7}$', modular_code):
        return responsesctl.response(400, message='Codigo de proyecto modular invalido')
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    if cursor:
        sql = '''SELECT * FROM modular_project WHERE modular_project_code = :1'''
        fetch = cursor.execute(sql, [modular_code])
        if fetch:
            tmp = fetch.fetchone()
            dbctl.close_connection()
            if tmp:
                modular = {
                    'modular_project_code': tmp[0],  # type: ignore
                    'degree_code': tmp[1],  # type: ignore
                    'modular_project_description': tmp[2],  # type: ignore
                    'last_update_date': tmp[3]  # type: ignore
                }
                return responsesctl.response(200, modular)
            return responsesctl.response(404, message='Proyecto modular no encontrado')
    dbctl.close_connection()
    return responsesctl.response(500, 
    message='Error al obtener informacion de los proyectos modulares')

@modularctl.route('/modular', methods=['POST'])
@token_required
def insert_modular(current_user):
    if not current_user:
        return responsesctl.response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return responsesctl.response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return responsesctl.response(401, message='Ruta no accesible (administrador inactivo)')
    data = request.get_json()
    if data:
        degree_code = data['degree_code'] #* Max length = 4 chars | uppercase | alphabetic
        modular_project_description = data['modular_project_description'] #* Max length = 1500 chars
        degree_code = degree_code.upper()
        if not re.match(r'^[A-Z]{4}$', degree_code):
            return responsesctl.response(400, message='Codigo de carrera invalido')
        if len(modular_project_description) > 1500:
            return responsesctl.response(400, 
            message='La descripcion del proyecto modular debe ser menor de 1500 caracteres')
        modular_project_code = f'mod{degree_code.lower()}'
        dbctl.open_connection()
        cursor = dbctl.get_cursor()
        if cursor:
            sql = '''INSERT INTO modular_project VALUES (:1, :2, :3, 
            NEW_TIME(SYSDATE, 'GMT', 'CST'))'''
            cursor.execute(sql, [modular_project_code, degree_code, modular_project_description])
            cursor.connection.commit()
            dbctl.close_connection()
            return responsesctl.response(200, 
            message=f'Proyecto modular agregado: {modular_project_code}')
        dbctl.close_connection()
    return responsesctl.response(500, message='Error al insertar un nuevo proyecto modular')

@modularctl.route('/modular/<modular_code>', methods=['PUT'])
@token_required
def update_modular(current_user, modular_code):
    if not current_user:
        return responsesctl.response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return responsesctl.response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return responsesctl.response(401, message='Ruta no accesible (administrador inactivo)')
    if not re.match(r'^[a-z]{7}$', modular_code):
        return responsesctl.response(400, message='Codigo de proyecto modular invalido')
    data = request.get_json()
    if data:
        modular_project_description = data['modular_project_description'] #* Max length = 1500 chars
        if len(modular_project_description) > 1500:
            return responsesctl.response(400, 
            message='La descripcion del proyecto modular debe ser menor de 1500 caracteres')
        dbctl.open_connection()
        cursor = dbctl.get_cursor()
        if cursor:
            sql = '''UPDATE modular_project SET modular_project_description = :1,
            last_update_date = NEW_TIME(SYSDATE, 'GMT', 'CST') 
            WHERE modular_project_code = :2'''
            cursor.execute(sql, [modular_project_description, modular_code])
            cursor.connection.commit()
            dbctl.close_connection()
            return responsesctl.response(200, message='Proyecto modular actualizado')
        dbctl.close_connection()
    return responsesctl.response(500, message='Error al actualizar el proyecto modular')
