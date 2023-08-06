# gumo-core

[![CircleCI](https://circleci.com/gh/gumo-py/gumo-core.svg?style=svg)](https://circleci.com/gh/gumo-py/gumo-core)

## Configuration

```python
from gumo.core import configure as core_configure

core_configure(
    google_cloud_project='<Google Cloud Platform Project Name>',
    google_cloud_location='<Project Main Location (Region)>',
)
```

If you need to load environment variables of app.yaml:

```python
import os
import flask
from gumo.core import MockAppEngineEnvironment
# from gumo.core import configure as core_configure


# The call to MockAppEngineEnvironment must precede any other initialization code.
if __name__ == '__main__':
    app_yaml_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'app.yaml'
    )
    MockAppEngineEnvironment.load_app_yaml(app_yaml_path=app_yaml_path)

# core_configure()

# Application Configurations ...
app = flask.Flask(__name__)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
```

## Setup Development Environment

```sh
$ git clone https://github.com/gumo-py/gumo-core.git
$ cd gumo-core

$ make setup
```

## Build and Test

```sh
$ make build

$ make test
```

## EntityKey

```python
from gumo.core import EntityKey
from gumo.core import EntityKeyFactory

key = EntityKeyFactory().build(kind='Book', name='978-1-4028-9462-6')

assert isinstance(key, EntityKey)
assert key.key_literal() == "Key('Book', '978-1-4028-9462-6')"
assert key.key_path() == 'Book:978-1-4028-9462-6'
assert key.key_url() == 'Book/978-1-4028-9462-6'
```
