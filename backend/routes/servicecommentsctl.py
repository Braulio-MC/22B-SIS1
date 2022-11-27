from flask import Blueprint, request
from jwtctl import token_required
from dbctl import DBContextManager
from responsesctl import response
from re import match


servicecommentsctl = Blueprint('servicecommentsctl', __name__)

def check_for_comment(student_code):
    with DBContextManager() as cursor:
        query = '''SELECT commentary_id FROM social_service_comments 
        WHERE CRYPTO_UTIL.DECRYPT(student_code) = :1'''
        cursor = cursor.execute(query, [student_code])
        data = cursor.fetchone()
        if data:
            return data[0]
    return None

@servicecommentsctl.route('/service-comments')
def get_all_service_comments():
    with DBContextManager() as cursor:
        output = []
        query = '''SELECT commentary_id, CRYPTO_UTIL.DECRYPT(student_code),
        commentary, publication_date FROM social_service_comments'''
        cursor = cursor.execute(query)
        data = cursor.fetchall()
        for val in data:
            output.append({
                'commentary_id': val[0],
                'student_code': val[1],
                'commentary': val[2],
                'publication_date': val[3]
            })
        return response(200, output)

@servicecommentsctl.route('/service_comments/<code>')
def get_service_comments_by_any_code(code):
    code = code.upper()
    column = ''
    if match(r'^SC[0-9]{1,}$', code):
        column = 'commentary_id'
    elif match(r'^[0-9]{9}$', code):
        column = 'student_code'
    else:
        return response(400, message='Codigo invalido')
    with DBContextManager() as cursor:
        query = f'''SELECT commentary_id, CRYPTO_UTIL.DECRYPT(student_code),
        commentary, publication_date FROM social_service_comments WHERE {column} = :1'''
        cursor = cursor.execute(query, [code])
        data = cursor.fetchone()
        if data:
            commentary = {
                'commentary_id': data[0],
                'student_code': data[1],
                'commentary': data[2],
                'publication_date': data[3]
            }
            return response(200, commentary)
        return response(404, message=f'No existe el comentario con id: {code}')

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
    client_data = request.get_json()
    if client_data:
        student_code = current_user['student_code']
        commentary = client_data['commentary']
        if not match(r'^[0-9]{9}$', student_code):
            return response(400, message='Codigo de estudiante invalido')
        if len(commentary) > 400:
            return response(400, message='El comentario debe ser menor de 400 caracteres')
        with DBContextManager() as cursor:
            query = '''INSERT INTO social_service_comments VALUES (
            CONCAT('SC', SEQ_SOCIAL_SERVICE_COMMENTS.nextval), 
            CRYPTO_UTIL.ENCRYPT(:1), :2, NEW_TIME(SYSDATE, 'GMT', 'CST'))'''
            cursor.execute(query, [student_code, commentary])
            cursor.connection.commit()
            return response(200, message='Comentario publicado')
    return response(400, message='Informacion para publicar el comentario no encontrada')

@servicecommentsctl.route('/service-comments', methods=['PUT'])
@token_required
def update_service_comment(current_user):
    if not current_user:
        return response(401, message='Token caducado o invalido')
    if not current_user['type'] == 'student':
        return response(401, message='Inicia sesion como estudiante')
    cid = check_for_comment(current_user['student_code'])
    if not cid:
        return response(404, message='Aun no has publicado un comentario')
    client_data = request.get_json()
    if client_data:
        commentary = client_data['commentary']
        if len(commentary) > 400:
            return response(400, message='El comentario debe ser menor de 400 caracteres')
        with DBContextManager() as cursor:
            query = '''UPDATE social_service_comments SET commentary = :1,
            publication_date = NEW_TIME(SYSDATE, 'GMT', 'CST')) WHERE commentary_id = :2'''
            cursor.execute(query, [commentary, cid])
            cursor.connection.commit()
            return response(200, message=f'Comentario actualizado con id {cid}')
    return response(400, message='Informacion para actualizar el comentario no encontrada')
