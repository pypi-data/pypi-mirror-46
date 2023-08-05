# python-agent

Python agent for [Scope](https://scope.undefinedlabs.com)


## Install

    pip install scopeagent


## Usage

First, get an API key from your Scope installation.

Then, prefix your startup command with `scope-run`:

    scope-run python run my_app.py
    scope-run gunicorn myapp.wsgi
    scope-run python -m unittest discover

### Parameters

| Flag | Required? | Default | Description | Environment variable |
|---|:---:|---|---|:---:|
| `-k`, `--apikey` | Y |  | API key tog use when sending data to Scope | `$SCOPE_APIKEY` |
| `-e`, `--api-endpoint` | Y |  | API endpoint of the Scope installation to send data to | `$SCOPE_API_ENDPOINT` |
| `-n`, `--name` | N | `default` | Service name to use when sending data to Scope | `$SCOPE_SERVICE` |
| `-c`, `--commit` | N | `$(git rev-parse HEAD)` | Commit hash to use when sending data to Scope | `$SCOPE_COMMIT_SHA` |
| `-r`, `--repository` | N | `$(git remote get-url origin)` | Repository URL to use when sending data to Scope | `$SCOPE_REPOSITORY` |
| `--root` | N | `$(git rev-parse --show-toplevel)` | Repository root path | `$SCOPE_SOURCE_ROOT` |

Commit, repository, and source root information will automatically be detected if running on CircleCI or Jenkins via environment variables.


### Advanced usage

If the above doesn't work for your specific setup, 
you can also install the Scope Agent by running the following as early as possible 
in your code (as it needs to patch supported libraries):

```python
import scopeagent

agent = scopeagent.Agent(api_key="xxxxxxxx", api_endpoint="https://scope.mycompany.corp")
agent.install()
```

### Supported libraries

Name | Span/event creation | Extract | Inject
-----|:-------------:|:-------:|:------:
[`celery`](http://www.celeryproject.org) | * |  |
[`gunicorn`](https://pypi.org/project/gunicorn/) | * | * |
[`requests`](https://pypi.org/project/requests/) | * | | *
[`unittest`](https://docs.python.org/3/library/unittest.html) | * | |
[`pytest`](https://pytest.org) | * | |
[`kombu`](https://github.com/celery/kombu) | * | * | *
[`logging`](https://docs.python.org/3/library/logging.html) | * | |


## Development

### Automated Testing
The following environment variables are used for database tests:

* `POSTGRES_DBURL`

## Acknowledgements

Some code is copied from or inspired by Uber's [opentracing-python-instrumentation
](https://github.com/uber-common/opentracing-python-instrumentation) (MIT license). The original copyright notice is maintained in copied files.
