# FlaskCerberus
Simple extension that enables Cerberus validation to a flask app.

## Useful Links
- Cerberus Docs: http://docs.python-cerberus.org/en/stable/index.html


### Example Usage

```python
from flask import Flask
from FlaskCerberus import FlaskCerberus

# see http://docs.python-cerberus.org/en/stable/index.html for
# more examples and documentation on Cerberus usage.
example_schema = {
    'name': {'type': 'string', 'required': True},
    'age': {'type': 'integer', 'required': True, 'min': 18}
}

app = Flask(__name__)
v = FlaskCerberus()

@app.route("/", methods=['GET', 'POST'])
@v.validate_post(example_schema, allow_unknown=False, require_all=False)
def hello():
    return Response(json.dumps({"hello":"world"}), status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run()
```

## Release History:

### `0.1rc1 - 05/12/19`
```
Updated extension to include methods that will validate query string parameters, post and put request.
Added automatic type inference based on isinstance.
Added basic request helper class.
```


### `0.1rc0 - 05/12/19`
```
Initial release. Basic POST request validation functionality started.
Learned a few hard lessons on naming packages in PyPi.
```