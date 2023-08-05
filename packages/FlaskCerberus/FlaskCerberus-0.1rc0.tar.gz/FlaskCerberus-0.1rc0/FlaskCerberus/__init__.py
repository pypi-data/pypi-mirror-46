from cerberus import Validator
from functools import wraps
from flask import request, Response
import json

class FlaskCerberus(object):
    def __init__(self, app=None):
        self.app = app
    
    def validate_post(self, schema=None, allow_unknown=False, require_all=False):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if request.method == 'POST':
                    if schema is not None:
                        data = False
                        is_valid = False
                        code = 400
                        
                        response = {}
                        response["body"] = {}
                        response["_meta"] = {}
                        response["_meta"]["reason"] = "no post data"
                        response["_meta"]["status_code"] = code
                        
                        
                        if request.mimetype == "application/json":
                            try:
                                data = request.get_json()
                            except Exception as err:
                                reason = str(err)
                        else:
                           response["_meta"]["reason"] = "mimetype must be set to application/json."

                        if data is not False:
                            v = Validator(schema, allow_unknown=allow_unknown, require_all=require_all)
                            is_valid = v.validate(data)
                            response["_meta"]["reason"] = "failed validation"
                            response["_meta"]["errors"] = v.errors
                        
                        if is_valid == False:    
                            return Response(json.dumps(response), status=code, mimetype='application/json')

                ctx = f(*args, **kwargs)
                return ctx
            return decorated_function
        return decorator