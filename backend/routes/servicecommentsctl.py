from flask import Blueprint, request
from jwtctl import token_required
from dbctl import DBCTL
from responsesctl import response
import re


servicecommentsctl = Blueprint('servicecommentsctl', __name__)
dbctl = DBCTL()

def check_for_comment(student_code):
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    if cursor:
        sql = '''SELECT commentary_id FROM social_service_comments 
        WHERE CRYPTO_UTIL.DECRYPT(student_code) = :1'''
        cursor = cursor.execute(sql, [student_code])
        if cursor:
            tmp = cursor.fetchone()
            if tmp:
                return tmp[0]  # type: ignore
    return None

@servicecommentsctl.route('/service-comments')
@token_required
def get_all_service_comments(current_user):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'student':
        return response(401, message='Inicia sesion como estudiante')
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    output = []
    if cursor:
        sql = '''SELECT commentary_id, CRYPTO_UTIL.DECRYPT(student_code),
        commentary, publication_date FROM social_service_comments'''
        cursor = cursor.execute(sql)
        if cursor:
            tmp = cursor.fetchall()
            dbctl.close_connection()
            for val in tmp:
                output.append({
                    'commentary_id': val[0],
                    'student_code': val[1],
                    'commentary': val[2],
                    'publication_date': val[3]
                })
            return response(200, output)
    dbctl.close_connection()
    return response(500, message='Error al obtener los comentarios del servicio social')

@servicecommentsctl.route('/service_comments/<code>')
@token_required
def get_one_service_comment_by_any_code(current_user, code):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'student':
        return response(401, message='Inicia sesion como estudiante')
    code = code.upper()
    column = ''
    if re.match(r'^SC[0-9]{1,}$', code):
        column = 'commentary_id'
    elif re.match(r'^[0-9]{9}$', code):
        column = 'student_code'
    else:
        return response(400, message='Codigo invalido')
    sql = f'''SELECT commentary_id, CRYPTO_UTIL.DECRYPT(student_code),
    commentary, publication_date FROM social_service_comments WHERE :1 = :2'''
    dbctl.open_connection()
    cursor = dbctl.get_cursor()
    if cursor:
        cursor = cursor.execute(sql, [column, code])
        if cursor:
            tmp = cursor.fetchone()
            dbctl.close_connection()
            if tmp:
                commentary = {
                    'commentary_id': tmp[0],  # type: ignore
                    'student_code': tmp[1],  # type: ignore
                    'commentary': tmp[2],  # type: ignore
                    'publication_date': tmp[3]  # type: ignore
                }
                return response(200, commentary)
    dbctl.close_connection()
    return response(500, message='Error al obtener el comentario del servicio social')

@servicecommentsctl.route('/service-comments', methods=['POST'])
@token_required
def add_service_comment(current_user):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'student':
        return response(401, message='Inicia sesion como estudiante')
    cid = check_for_comment(current_user['student_code'])
    if cid:
        return response(400, message=f'Comentario ya publicado con id: {cid}')
    data = request.get_json()
    if data:
        student_code = current_user['student_code']
        commentary = data['commentary']
        if not re.match(r'^[0-9]{9}$', student_code):
            return response(400, message='Codigo de estudiante invalido')
        if len(commentary) > 400:
            return response(400, message='El comentario debe ser menor de 400 caracteres')
        dbctl.open_connection()
        cursor = dbctl.get_cursor()
        if cursor:
            sql = '''INSERT INTO social_service_comments VALUES (
            CONCAT('SC', SEQ_SOCIAL_SERVICE_COMMENTS.nextval), 
            CRYPTO_UTIL.ENCRYPT(:1), :2, NEW_TIME(SYSDATE, 'GMT', 'CST'))'''
            cursor.execute(sql, [student_code, commentary])
            cursor.connection.commit()
            dbctl.close_connection()
            return response(200, message='Comentario agregado')
        dbctl.close_connection()
    return response(500, message='Error al agregar un comentario al servicio')

@servicecommentsctl.route('/service-comments/<cid>', methods=['PUT'])
@token_required
def update_service_comment(current_user, cid):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'student':
        return response(401, message='Inicia sesion como estudiante')
    if not re.match(r'^SC[0-9]{1,}$', cid):
        return response(400, message='ID de comentario invalido')
    data = request.get_json()
    if data:
        commentary = data['commentary']
        if len(commentary) > 400:
            return response(400, message='El comentario debe ser menor de 400 caracteres')
        dbctl.open_connection()
        cursor = dbctl.get_cursor()
        if cursor:
            sql = '''UPDATE social_service_comments SET commentary = :1 
            WHERE commentary_id = :2'''
            cursor.execute(sql, [commentary, cid])
            cursor.connection.commit()
            dbctl.close_connection()
            return response(200, message='Comentario actualizado')
        dbctl.close_connection()
    return response(500, message=f'Error al modificar el comentario con id: {cid}')
