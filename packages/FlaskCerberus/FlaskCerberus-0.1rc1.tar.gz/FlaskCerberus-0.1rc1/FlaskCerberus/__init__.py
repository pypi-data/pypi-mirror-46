from cerberus import Validator
from functools import wraps
from flask import request, Response
import json
from pydoc import locate
from pprint import pprint

class Decoder(json.JSONDecoder):
    """ infer proper type from given string """
    def decode(self, s):
        result = super().decode(s)
        return self._decode(result)

    def _decode(self, o):
        if isinstance(o, str):
            try:
                return int(o)
            except ValueError:
                try:
                    return float(o)
                except ValueError:
                    return o
        elif isinstance(o, dict):
            return {k: self._decode(v) for k, v in o.items()}
        elif isinstance(o, list):
            return [self._decode(v) for v in o]
        else:
            return o

class R(Response):
    """ response helper """
    def __init__(self):
        self.r = {}
        self.r["data"] = {}
        self.r["_meta"] = {}
        self.r["_meta"]["reason"] = "no document to validate"
    
    def _set_reason(self, reason):
        self.r["_meta"]["reason"] = reason
    
    def _set_errors(self, error):
        if error:
            k = list(error.keys())[0]
            v = error[k][0]
            self.r["_meta"]["error"] = {"field": k, "error": v}

    def send(self, code=400):
        self.r["_meta"]["status_code"] = code
        return Response(json.dumps(self.r), status=code, mimetype='application/json')
    

class FlaskCerberus(object):
    """ add Cerberus validation to flask routes via decorators """
    def __init__(self, app=None):
        self.app = app

    def validate_query_string(self, schema=None, allow_unknown=False, require_all=False):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if schema is not None:
                    # data = False
                    is_valid = False
                    r = R()
                    # if len(request.args) > 0:
                    data = json.loads(json.dumps(request.args), cls=Decoder)
                    if data is not False:
                        v = Validator(schema, allow_unknown=allow_unknown, require_all=require_all)
                        is_valid = v.validate(data)
                        r._set_reason("failed validation")
                        r._set_errors(v.errors)
                    
                    if is_valid == False:    
                        return r.send()
                    else:
                        for d in data:
                            kwargs[d] = data[d]
                    
                ctx = f(*args, **kwargs)
                return ctx
            return decorated_function
        return decorator

    def validate_post_request(self, schema=None, allow_unknown=False, require_all=False):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if request.method == 'POST':
                    if schema is not None:
                        data = False
                        is_valid = False
                        r = R()
                    
                        if request.mimetype == "application/json":
                            try:
                                data = request.get_json()
                            except Exception as err:
                                r._set_reason(str(err))
                        else:
                           r.r["_meta"]["reason"] = "mimetype must be set to application/json."

                        if data is not False:
                            v = Validator(schema, allow_unknown=allow_unknown, require_all=require_all)
                            is_valid = v.validate(data)
                            r._set_reason("failed validation")
                            r._set_errors(v.errors)
                        
                        if is_valid == False:    
                            return r.send()
                        else:
                            for d in data:
                                kwargs[d] = data[d]
                ctx = f(*args, **kwargs)
                return ctx
            return decorated_function
        return decorator

    def validate_put_request(self, schema=None, allow_unknown=False, require_all=False):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if request.method == 'PUT' or request.method == 'PATCH':
                    if schema is not None:
                        data = False
                        is_valid = False
                        r = R()
                    
                        if request.mimetype == "application/json":
                            try:
                                data = request.get_json()
                            except Exception as err:
                                r._set_reason(str(err))
                        else:
                           r.r["_meta"]["reason"] = "mimetype must be set to application/json."

                        if data is not False:
                            v = Validator(schema, allow_unknown=allow_unknown, require_all=require_all)
                            is_valid = v.validate(data)
                            r._set_reason("failed validation")
                            r._set_errors(v.errors)
                        
                        if is_valid == False:    
                            return r.send()
                        else:
                            for d in data:
                                kwargs[d] = data[d]
                ctx = f(*args, **kwargs)
                return ctx
            return decorated_function
        return decorator