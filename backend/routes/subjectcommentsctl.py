from flask import Blueprint, request
from jwtctl import token_required
from dbctl import DBCTL
from responsesctl import response
import re


subjectcommentsctl = Blueprint('subjectcommentsctl', __name__)
dbctl = DBCTL()

"""
Nombre           ¿Nulo?   Tipo          
---------------- -------- ------------- 
COMMENTARY_ID    NOT NULL NUMBER(38)    
CVE                       VARCHAR2(5)   
STUDENT_CODE              VARCHAR2(9)   
COMMENTARY                VARCHAR2(400) 
GRADE                     NUMBER(38)    
PUBLICATION_DATE          DATE    

current_user = {
    'student_code': data['student_code'],
    'student_name': tmp[0],  # type: ignore
    'degree_code': tmp[1],  # type: ignore
    'degree_name': tmp[2],  # type: ignore
    'creation_date': tmp[3],  # type: ignore
    'type': data['type']
}
"""

def check_for_comment(student_code):
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    if cursor:
        sql = '''SELECT commentary_id FROM subject_comments 
        WHERE CRYPTO_UTIL.DECRYPT(student_code) = :1'''
        cursor = cursor.execute(sql, [student_code])
        if cursor:
            tmp = cursor.fetchone()
            if tmp:
                return tmp[0]  # type: ignore
    return None

@subjectcommentsctl.route('/subject-comments')
@token_required
def get_all_subject_comments(current_user):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'student':
        return response(401, message='Inicia sesion como estudiante')
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    output = []
    if cursor:
        sql = '''SELECT commentary_id, cve, CRYPTO_UTIL.DECRYPT(student_code), 
        commentary, grade, publication_date FROM subject_comments'''
        fetch = cursor.execute(sql)
        if fetch:
            tmp = fetch.fetchall()
            dbctl.close_connection()
            for val in tmp:
                output.append({
                    'commentary_id': val[0],
                    'cve': val[1],
                    'student_code': val[2],
                    'commentary': val[3],
                    'grade': val[4],
                    'publication_date': val[5]
                })
            return response(200, output)
    dbctl.close_connection()
    return response(500, message='Error al obtener los comentarios')

@subjectcommentsctl.route('/subject-comments/<code>')
@token_required
def get_one_subject_comment_by_any_code(current_user, code): #! VERIFY FUNCTIONALITY
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'student':
        return response(401, message='Inicia sesion como estudiante')
    code = code.upper()
    column = ''
    if re.match(r'^SC[0-9]{1,}$', code):
        column = 'commentary_id'
    elif re.match(r'^I[0-9]{4}$', code):
        column = 'cve' #! RETURN ALL COMMENTARIES BY CVE
    elif re.match(r'^[0-9]{9}$', code):
        column = 'student_code'
    else:
        return response(400, message='Codigo invalido')
    sql = f'''SELECT commentary_id, cve, CRYPTO_UTIL.DECRYPT(student_code), 
    commentary, grade, publication_date FROM subject_comments WHERE :1 = :2'''
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    output = []
    if cursor:
        fetch = cursor.execute(sql, [column, code])
        if fetch:
            if column == 'cve':
                tmp = fetch.fetchall()
                dbctl.close_connection()
                for val in tmp:
                    output.append({
                        'commentary_id': val[0],
                        'cve': val[1],
                        'student_code': val[2],
                        'commentary': val[3],
                        'grade': val[4],
                        'publication_date': val[5]
                    })
                return response(200, output)
            else:
                tmp = fetch.fetchone()
                dbctl.close_connection()
                if tmp:
                    commentary = {
                        'commentary_id': tmp[0],  # type: ignore
                        'cve': tmp[1],  # type: ignore
                        'student_code': tmp[2],  # type: ignore
                        'commentary': tmp[3],  # type: ignore
                        'grade': tmp[4],  # type: ignore
                        'publication_date': tmp[5]  # type: ignore
                    }
                    return response(200, commentary)
    dbctl.close_connection()
    return response(500, message='Error al obtener el comentario')

@subjectcommentsctl.route('/subject-comments', methods=['POST'])
@token_required
def add_subject_comment(current_user):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'student':
        return response(401, message='Inicia sesion como estudiante')
    cid = check_for_comment(current_user['student_code'])
    if cid:
        return response(400, message=f'Comentario ya publicado con id: {cid}')
    data = request.get_json()
    if data:
        cve = data['cve']
        student_code = current_user['student_code']
        commentary = data['commentary']
        grade = data['grade']
        if not re.match(r'^I[0-9]{4}$', cve):
            return response(400, message='Codigo de materia invalido')
        if not re.match(r'^[0-9]{9}$', student_code):
            return response(400, message='Codigo de estudiante invalido')
        if len(commentary) > 400:
            return response(400, message='El comentario debe ser menor de 400 caracteres')
        if grade > 5:
            return response(400, message='La calificacion debe estar entre 1 y 5')
        dbctl.open_connection()
        cursor = dbctl.get_cursor()
        if cursor:
            sql = '''INSERT INTO SUBJECT_COMMENTS VALUES (
            CONCAT('SC',SEQ_SUBJECT_COMMENTS.nextval),
            :1, CRYPTO_UTIL.ENCRYPT(:2), :3, :4, NEW_TIME(SYSDATE, 'GMT', 'CST'))'''
            cursor.execute(sql, [cve, student_code, commentary, grade])
            cursor.connection.commit()
            dbctl.close_connection()
            return response(200, message='Comentario agregado')
        dbctl.close_connection()
    return response(500, message='Error al agregar un comentario a la materia')

@subjectcommentsctl.route('/subject-comments/<cid>', methods=['PUT'])
@token_required
def update_subject_comment(current_user, cid):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'student':
        return response(401, message='Inicia sesion como estudiante')
    if not re.match(r'^SC[0-9]{1,}$', cid):
        return response(400, message='ID de comentario invalido')
    data = request.get_json()
    if data:
        commentary = data['commentary']
        grade = data['grade']
        if len(commentary) > 400:
            return response(400, 
            message='El comentario debe ser menor de 400 caracteres')
        if grade > 5:
            return response(400, message='La calificacion debe estar entre 1 y 5')
        dbctl.open_connection()
        cursor = dbctl.get_cursor()
        if cursor:
            sql = '''UPDATE subject_comments SET commentary = :1, grade = :2, 
            publication_date = NEW_TIME(SYSDATE, 'GMT', 'CST') WHERE commentary_id = :3'''
            cursor.execute(sql, [commentary, grade, cid])
            cursor.connection.commit()
            dbctl.close_connection()
            return response(200, message='Comentario actualizado')
        dbctl.close_connection()
    return response(500, message=f'Error al modificar el comentario con id: {cid}')
