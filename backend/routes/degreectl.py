from flask import Blueprint, request
from dbctl import DBCTL
from jwtctl import token_required
import responsesctl
import re


degreectl = Blueprint('degreectl', __name__)
dbctl = DBCTL()

@degreectl.route('/degree')
def get_all_degrees():
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    output = []
    if cursor:
        sql = '''SELECT * FROM degree'''
        fetch = cursor.execute(sql)
        if fetch:
            result = fetch.fetchall()
            dbctl.close_connection()
            for val in result:
                output.append({
                    'degree_code': val[0],
                    'degree_name': val[1],
                    'degree_description': val[2],
                    'no_subjects': val[3],
                    'no_semesters': val[4],
                    'last_update_date': val[5]
                })
            return responsesctl.response(200, output)
    dbctl.close_connection()
    return responsesctl.response(500, message='Error al obtener la informacion de carreras')

@degreectl.route('/degree/<degree_code>')
def get_one_degree(degree_code):
    degree_code = degree_code.upper()
    if not re.match(r'^[A-Z]{4}$', degree_code):
        return responsesctl.response(400, message='Codigo invalido')
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    if cursor:
        sql = '''SELECT * FROM degree WHERE degree_code = :1'''
        fetch = cursor.execute(sql, [degree_code])
        if fetch:
            result = fetch.fetchone()
            dbctl.close_connection()
            if result:
                subject = {
                        'degree_code': result[0],  # type: ignore
                        'degree_name': result[1],  # type: ignore
                        'degree_description': result[2],  # type: ignore
                        'no_subjects': result[3],  # type: ignore
                        'no_semesters': result[4],  # type: ignore
                        'last_update_date': result[5]  # type: ignore
                    }
                return responsesctl.response(200, subject)
    dbctl.close_connection()
    return responsesctl.response(500, message='Error al obtener la informacion de la carrera')

@degreectl.route('/degree', methods=['POST'])
@token_required
def insert_degree(current_user):
    if not current_user:
        return responsesctl.response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return responsesctl.response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return responsesctl.response(401, message='Ruta no accesible (administrador inactivo)')
    data = request.get_json()
    if data:
        degree_code = data['degree_code'] #* Max length = 4 chars | uppercase | alphabetic
        degree_name = data['degree_name'] #* Max length = 60 chars
        degree_description = data['degree_description'] #* Max length = 900 chars
        no_subjects = data['no_subjects'] #* Check for the largest number of subjects
        no_semesters = data['no_semesters'] #* Check for the largest number of semesters
        degree_code = degree_code.upper()
        if not re.match(r'^[A-Z]{4}$', degree_code):
            return responsesctl.response(400, message='Codigo invalido')
        if len(degree_name) > 60:
            return responsesctl.response(400,
            message='El nombre de carrera debe ser menor a 60 caracteres')
        if len(degree_description) > 900:
            return responsesctl.response(400, 
            message='La descripcion de carrera debe ser menor a 900 caracteres')
        dbctl.open_connection()
        cursor = dbctl.get_cursor()
        if cursor:
            sql = '''INSERT INTO degree VALUES (:1, :2, :3, :4, :5, 
            NEW_TIME(SYSDATE, 'GMT', 'CST'))'''
            cursor.execute(sql, [degree_code, degree_name, degree_description, 
            no_subjects, no_semesters])
            cursor.connection.commit()
            dbctl.close_connection()
            return responsesctl.response(200, message='Carrera agregada')
        dbctl.close_connection()
    return responsesctl.response(500, message='Error al agregar una nueva carrera')

#? Keep in mind that client-side will send degree_code in a correct way: 4 chars | alphabetic
#? So validate the presence of degree_code on DB here is not necessary
@degreectl.route('/degree/<degree_code>', methods=['PUT'])
@token_required
def update_degree(current_user, degree_code):
    if not current_user:
        return responsesctl.response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return responsesctl.response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return responsesctl.response(401, message='Ruta no accesible (administrador inactivo)')
    degree_code = degree_code.upper()
    if not re.match(r'^[A-Z]{4}$', degree_code):
        return responsesctl.response(400, message='Codigo invalido')
    """ if get_one_degree(degree_code).status_code != 200:
        return responsesctl.response(404, 
        message='El codigo de carrera dado no existe') """
    data = request.get_json()
    if data:
        degree_name = data['degree_name'] #* Max length = 60 chars
        degree_description = data['degree_description'] #* Max length = 900 chars
        no_subjects = data['no_subjects'] #* Check for the largest number of subjects
        no_semesters = data['no_semesters'] #* Check for the largest number of semesters
        if len(degree_name) > 60:
            return responsesctl.response(400,
            message='El nombre de carrera debe ser menor a 60 caracteres')
        if len(degree_description) > 900:
            return responsesctl.response(400, 
            message='La descripcion de carrera debe ser menor a 900 caracteres')
        dbctl.open_connection()
        cursor = dbctl.get_cursor()
        if cursor:
            sql = '''UPDATE degree SET degree_name = :1, degree_description = :2, 
            no_subjects = :3, no_semesters = :4, 
            last_update_date = NEW_TIME(SYSDATE, 'GMT', 'CST') WHERE degree_code = :5'''
            cursor.execute(sql, [degree_name, degree_description, no_subjects, 
            no_semesters, degree_code])
            cursor.connection.commit()
            dbctl.close_connection()
            return responsesctl.response(200, message='Carrera modificada')
        dbctl.close_connection()
    return responsesctl.response(500, message='Error al actualizar la carrera')