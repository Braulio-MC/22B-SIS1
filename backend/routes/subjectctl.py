from flask import Blueprint
from dbctl import DBCTL
import responsesctl
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
        fetch = cursor.execute(sql)
        if fetch:
            tmp = fetch.fetchall()
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
            return responsesctl.response(200, output)
    dbctl.close_connection()
    return responsesctl.response(500, message='Error al obtener la informacion de materias')

@subjectctl.route('/subject/<code>')
def get_all_subjects_by_any_code(code):
    code = code.upper()
    if re.match(r'^I[0-9]{4}$', code):
        dbctl.open_connection()
        cursor = dbctl.get_cursor()
        output = []
        if cursor:
            sql = '''SELECT * FROM subject WHERE cve = :1'''
            fetch = cursor.execute(sql, [code])
            if fetch:
                tmp = fetch.fetchall()
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
                return responsesctl.response(200, output)
        dbctl.close_connection()
    elif re.match(r'^[A-Z]{4}$', code):
        dbctl.open_connection()
        cursor = dbctl.get_cursor()
        output = []
        if cursor:
            sql = '''SELECT * FROM subject WHERE degree_code = :1'''
            fetch = cursor.execute(sql, [code])
            if fetch:
                tmp = fetch.fetchall()
                dbctl.close_connection()
                for val in tmp:
                    output.append({
                        'CVE': val[0],
                        'degree_code': code,
                        'subject_name': val[2],
                        'subject_description': val[3],
                        'subject_semester': val[4],
                        'subject_type': val[5],
                        'subject_credits': val[6],
                        'last_update_date': val[7]
                    })
                return responsesctl.response(200, output)
        dbctl.close_connection()
    return responsesctl.response(400, message='Codigo invalido')

@subjectctl.route('/subject/<degree_code>/<subject_code>')
def get_one_subject(degree_code, subject_code):
    degree_code = degree_code.upper()
    subject_code = subject_code.upper()
    if not re.match(r'^[A-Z]{4}$', degree_code):
        return responsesctl.response(400, message='Codigo de carrera invalido')
    if not re.match(r'^I[0-9]{4}$', subject_code):
        return responsesctl.response(400, message='Codigo de materia invalido')
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    if cursor:
        sql = '''SELECT * FROM subject WHERE cve = :1 AND degree_code = :2'''
        fetch = cursor.execute(sql, [subject_code, degree_code])
        if fetch:
            result = fetch.fetchone()
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
                return responsesctl.response(200, subject)
            return responsesctl.response(404, message='Materia no encontrada')
    dbctl.close_connection()
    return responsesctl.response(500, message='Error al obtener la informacion de la materia')

#? INSERT, UPDATE