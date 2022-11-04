from flask import jsonify

def response(status_code: int, *args, **kwargs):
    if args:
        response = jsonify(*args)
        response.status_code = status_code
        return response
    response = jsonify (**kwargs)
    response.status_code = status_code
    return response
