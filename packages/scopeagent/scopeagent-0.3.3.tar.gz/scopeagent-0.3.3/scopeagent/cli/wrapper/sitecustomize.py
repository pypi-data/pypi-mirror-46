import os
import shlex
import sys
argv = shlex.split(os.getenv('SCOPE_COMMAND'))
if len(argv) >= 3 and argv[0] == 'python':
    if argv[1] == '-m':
        argv = ["python -m %s" % argv[2]] + argv[3:]
    else:
        argv = argv[1:]
sys.argv = argv

import scopeagent


agent = scopeagent.Agent(
    api_key=os.getenv('SCOPE_APIKEY'),
    api_endpoint=os.getenv('SCOPE_API_ENDPOINT'),
    service=os.getenv('SCOPE_SERVICE'),
    debug='SCOPE_DEBUG' in os.environ,
    command=os.getenv('SCOPE_COMMAND'),
    dry_run='SCOPE_DRYRUN' in os.environ,
)
agent.install()
