from flask import request
from jwt import encode, decode, exceptions as ex
from datetime import datetime, timedelta, timezone
from os import getenv
import responsesctl as responsesctl
from functools import wraps
from dbctl import DBCTL


dbctl = DBCTL()

def expiration_date(mins: int = 30):
    return datetime.now(tz=timezone.utc) + timedelta(minutes=mins)

def generate(data: dict):
    payload = {
        **data,
        'exp': expiration_date()
    }
    token = encode(payload=payload, key=getenv('SECRET_KEY'), algorithm='HS256')  # type: ignore
    return token

def verify(token: str):
    try:
        return decode(token, key=getenv('SECRET_KEY'), algorithms=['HS256'])  # type: ignore
    except ex.DecodeError:
        return responsesctl.response(401, message='Token invalido')
    except ex.ExpiredSignatureError:
        return responsesctl.response(401, message='Token caducado')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return responsesctl.response(401, 
            message='Token de autenticacion no proporcionado')
        current_user = None
        data = verify(token)
        if type(data) is dict:
            dbctl.open_connection()
            cursor = dbctl.get_cursor()
            if cursor:
                if data['type'] == 'student':
                    sql = '''SELECT CRYPTO_UTIL.DECRYPT(student.student_name), 
                    student.degree_code, degree.degree_name, student.creation_date
                    FROM ADMIN.student INNER JOIN ADMIN.degree 
                    ON student.degree_code = degree.degree_code 
                    WHERE CRYPTO_UTIL.DECRYPT(student.student_code) = :1'''
                    fetch = cursor.execute(sql, [data['student_code']])
                    if fetch:
                        tmp = fetch.fetchone()
                        if tmp:
                            current_user = {
                                'student_code': data['student_code'],
                                'student_name': tmp[0],  # type: ignore
                                'degree_code': tmp[1],  # type: ignore
                                'degree_name': tmp[2],  # type: ignore
                                'creation_date': tmp[3],  # type: ignore
                                'type': data['type']
                            }
                elif data['type'] == 'admin':
                    sql = '''SELECT CRYPTO_UTIL.DECRYPT(admin_name), admin_status, 
                    creation_date FROM admin WHERE CRYPTO_UTIL.DECRYPT(admin_code) = :1'''
                    fetch = cursor.execute(sql, [data['admin_code']])
                    if fetch:
                        tmp = fetch.fetchone()
                        if tmp:
                            current_user = {
                                'admin_code': data['admin_code'],
                                'admin_name': tmp[0],  # type: ignore
                                'admin_status': tmp[1],  # type: ignore
                                'creation_date': tmp[2],  # type: ignore
                                'type': data['type']
                            }
            dbctl.close_connection()
        return f(current_user, *args, **kwargs)
    return decorated
