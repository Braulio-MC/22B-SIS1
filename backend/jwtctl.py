from flask import request
from jwt import encode, decode, exceptions as ex
from datetime import datetime, timedelta, timezone
from os import getenv
from responsesctl import response
from functools import wraps
from dbctl import DBContextManager
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

def expiration_date(mins: int = 30):
    return datetime.now(tz=timezone.utc) + timedelta(minutes=mins)

def generate(data: dict):
    payload = {
        **data,
        'exp': expiration_date()
    }
    token = encode(payload=payload, key=getenv('SECRET_KEY'), algorithm='HS256')
    return token

def verify(token: str):
    try:
        return decode(token, key=getenv('SECRET_KEY'), algorithms=['HS256'])
    except ex.DecodeError:
        return response(401, message='Token invalido')
    except ex.ExpiredSignatureError:
        return response(401, message='Token caducado')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return response(401, 
            message='Token de autenticacion no proporcionado')
        current_user = None
        token_data = verify(token)
        if type(token_data) is dict:
            with DBContextManager() as cursor:
                if token_data['type'] == 'student':
                    query = '''SELECT CRYPTO_UTIL.DECRYPT(student.student_name), 
                    student.degree_code, degree.degree_name, student.creation_date
                    FROM student INNER JOIN degree 
                    ON student.degree_code = degree.degree_code 
                    WHERE CRYPTO_UTIL.DECRYPT(student.student_code) = :1'''
                    student_code = token_data['student_code']
                    cursor = cursor.execute(query, [student_code])
                    data = cursor.fetchone()
                    if data:
                        current_user = {
                            'student_code': student_code,
                            'student_name': data[0],
                            'degree_code': data[1],
                            'modular_code': f'MOD{data[1]}',
                            'degree_name': data[2],
                            'creation_date': data[3],
                            'type': token_data['type']
                        }
                elif token_data['type'] == 'admin':
                    query = '''SELECT CRYPTO_UTIL.DECRYPT(admin_name), admin_status, 
                    creation_date FROM admin WHERE CRYPTO_UTIL.DECRYPT(admin_code) = :1'''
                    admin_code = token_data['admin_code']
                    cursor = cursor.execute(query, [admin_code])
                    data = cursor.fetchone()
                    if data:
                        current_user = {
                            'admin_code': admin_code,
                            'admin_name': data[0],
                            'admin_status': data[1],
                            'creation_date': data[2],
                            'type': token_data['type']
                        }
        return f(current_user, *args, **kwargs)
    return decorated
