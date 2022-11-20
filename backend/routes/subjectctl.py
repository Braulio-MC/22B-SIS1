from flask import Blueprint, request
from dbctl import DBCTL
from responsesctl import response
from jwtctl import token_required
import re


subjectctl = Blueprint('subjectctl', __name__)
dbctl = DBCTL()

@subjectctl.route('/subject')
def get_all_subjects():
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    output = []
    if cursor:
        sql = '''SELECT * FROM subject'''
        cursor = cursor.execute(sql)
        if cursor:
            tmp = cursor.fetchall()
            dbctl.close_connection()
            for val in tmp:
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
    dbctl.close_connection()
    return response(500, message='Error al obtener la informacion de materias')

@subjectctl.route('/subject/<code>')
def get_all_subjects_by_any_code(code):
    code = code.upper()
    column = ''
    if re.match(r'^I[0-9]{4}$', code):
        column = 'cve'
    elif re.match(r'^[A-Z]{4}$', code):
        column = 'degree_code'
    else:
        return response(400, message='Codigo invalido')
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    output = []
    if cursor:
        sql = '''SELECT * FROM subject WHERE :1 = :2'''
        cursor = cursor.execute(sql, [column, code])
        if cursor:
            tmp = cursor.fetchall()
            dbctl.close_connection()
            for val in tmp:
                output.append({
                    'CVE': code,
                    'degree_code': val[1],
                    'subject_name': val[2],
                    'subject_description': val[3],
                    'subject_semester': val[4],
                    'subject_type': val[5],
                    'subject_credits': val[6],
                    'last_update_date': val[7]
                })
            return response(200, output)
    dbctl.close_connection()
    return response(400, message='Codigo invalido')

@subjectctl.route('/subject/<degree_code>/<subject_code>')
def get_one_subject(degree_code, subject_code):
    degree_code = degree_code.upper()
    subject_code = subject_code.upper()
    if not re.match(r'^[A-Z]{4}$', degree_code):
        return response(400, message='Codigo de carrera invalido')
    if not re.match(r'^I[0-9]{4}$', subject_code):
        return response(400, message='Codigo de materia invalido')
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    if cursor:
        sql = '''SELECT * FROM subject WHERE cve = :1 AND degree_code = :2'''
        cursor = cursor.execute(sql, [subject_code, degree_code])
        if cursor:
            result = cursor.fetchone()
            dbctl.close_connection()
            if result:
                subject = {
                    'CVE': subject_code,
                    'degree_code': degree_code,
                    'subject_name': result[2],  #type: ignore
                    'subject_description': result[3],  #type: ignore
                    'subject_semester': result[4],  #type: ignore
                    'subject_type': result[5],  #type: ignore
                    'subject_credits': result[6],  #type: ignore
                    'last_update_date': result[7]  #type: ignore
                }
                return response(200, subject)
            return response(404, message='Materia no encontrada')
    dbctl.close_connection()
    return response(500, message='Error al obtener la informacion de la materia')

@subjectctl.route('/subject', methods=['POST'])
@token_required
def add_subject(current_user):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'admin':
        return response(401, message='Ruta no accesible')
    if not current_user['admin_status'] == 1:
        return response(401, message='Ruta no accesible (administrador inactivo)')
    data = request.get_json()
    if data:
        CVE = data['cve']
        degree_code = data['degree_code']
        subject_name = data['subject_name']
        subject_description = data['subject_description']
        subject_semester =  data['subject_semester']
        subject_type = data['subject_type']
        subject_credits = data['subject_credits']
        
    return response(500, message='Error al agregar una materia')

#? INSERT, UPDATE