from flask import Blueprint, request
from jwtctl import token_required
from dbctl import DBContextManager
from responsesctl import response
from re import match


subjectcommentsctl = Blueprint('subjectcommentsctl', __name__)

def check_for_comment(student_code):
    with DBContextManager() as cursor:
        query = '''SELECT commentary_id FROM subject_comments 
        WHERE CRYPTO_UTIL.DECRYPT(student_code) = :1'''
        cursor = cursor.execute(query, [student_code])
        data = cursor.fetchone()
        if data:
            return data[0]
    return None

@subjectcommentsctl.route('/subject-comments')
def get_all_subject_comments():
    with DBContextManager() as cursor:
        output = []
        query = '''SELECT commentary_id, cve, CRYPTO_UTIL.DECRYPT(student_code), 
        commentary, grade, publication_date FROM subject_comments'''
        cursor = cursor.execute(query)
        data = cursor.fetchall()
        for val in data:
            output.append({
                'commentary_id': val[0],
                'cve': val[1],
                'student_code': val[2],
                'commentary': val[3],
                'grade': val[4],
                'publication_date': val[5]
            })
        return response(200, output)

@subjectcommentsctl.route('/subject-comments/<code>')
def get_subject_comments_by_any_code(code):
    code = code.upper()
    column = ''
    if match(r'^SC[0-9]{1,}$', code):
        column = 'commentary_id'
    elif match(r'^I[0-9]{4}$', code):
        column = 'cve'
    elif match(r'^[0-9]{9}$', code):
        column = 'student_code'
    else:
        return response(400, message='Codigo invalido')
    with DBContextManager() as cursor:
        query = f'''SELECT commentary_id, cve, CRYPTO_UTIL.DECRYPT(student_code), 
        commentary, grade, publication_date FROM subject_comments WHERE {column} = :1'''
        cursor = cursor.execute(query, [code])
        if column == 'cve':
            output = []
            data = cursor.fetchall()
            for val in data:
                output.append({
                    'commentary_id': val[0],
                    'cve': val[1],
                    'student_code': val[2],
                    'commentary': val[3],
                    'grade': val[4],
                    'publication_date': val[5]
                })
            return response(200, output)
        data = cursor.fetchone()
        if data:
            commentary = {
                'commentary_id': data[0],
                'cve': data[1],
                'student_code': data[2],
                'commentary': data[3],
                'grade': data[4],
                'publication_date': data[5]
            }
            return response(200, commentary)
        return response(404, message=f'No existe el comentario con id: {code}')

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
    client_data = request.get_json()
    if client_data:
        cve = client_data['cve']
        student_code = current_user['student_code']
        commentary = client_data['commentary']
        grade = client_data['grade']
        if not match(r'^I[0-9]{4}$', cve):
            return response(400, message='Codigo de materia invalido')
        if not match(r'^[0-9]{9}$', student_code):
            return response(400, message='Codigo de estudiante invalido')
        if len(commentary) > 400:
            return response(400, message='El comentario debe ser menor de 400 caracteres')
        if grade > 5:
            return response(400, message='La calificacion debe estar entre 1 y 5')
        with DBContextManager() as cursor:
            query = '''INSERT INTO SUBJECT_COMMENTS VALUES (
            CONCAT('SC',SEQ_SUBJECT_COMMENTS.nextval),
            :1, CRYPTO_UTIL.ENCRYPT(:2), :3, :4, NEW_TIME(SYSDATE, 'GMT', 'CST'))'''
            cursor.execute(query, [cve, student_code, commentary, grade])
            cursor.connection.commit()
            return response(200, message='Comentario publicado')
    return response(400, message='Informacion para publicar el comentario no encontrada')

@subjectcommentsctl.route('/subject-comments', methods=['PUT'])
@token_required
def update_subject_comment(current_user):
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
        grade = client_data['grade']
        if len(commentary) > 400:
            return response(400, 
            message='El comentario debe ser menor de 400 caracteres')
        if grade > 5:
            return response(400, message='La calificacion debe estar entre 1 y 5')
        with DBContextManager() as cursor:
            query = '''UPDATE subject_comments SET commentary = :1, grade = :2, 
            publication_date = NEW_TIME(SYSDATE, 'GMT', 'CST') WHERE commentary_id = :3'''
            cursor.execute(query, [commentary, grade, cid])
            cursor.connection.commit()
            return response(200, message=f'Comentario actualizado con id {cid}')
    return response(400, message='Informacion para actualizar el comentario no encontrada')
