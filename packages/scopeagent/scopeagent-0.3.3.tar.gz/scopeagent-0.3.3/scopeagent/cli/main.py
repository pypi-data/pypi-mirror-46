import argparse
import logging
import os
import subprocess
from .. import version


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Run an application with automatic Scope instrumentation')
    parser.add_argument("--apikey", "-k", type=str, required=False, default=os.getenv('SCOPE_APIKEY'), dest='apikey',
                        help="API key to use when sending data to Scope [$SCOPE_APIKEY]")
    parser.add_argument("--api-endpoint", "-e", type=str, required=False, default=os.getenv('SCOPE_API_ENDPOINT'),
                        dest='api_endpoint',
                        help="API endpoint of the Scope installation to send data to [$SCOPE_API_ENDPOINT]")
    parser.add_argument("--name", "-n", type=str, required=False, default=os.getenv('SCOPE_SERVICE'), dest='name',
                        help="Service name to use when sending data to Scope [$SCOPE_SERVICE]")
    parser.add_argument("--commit", "-c", type=str, required=False, default=os.getenv('SCOPE_COMMIT_SHA'), dest='commit',
                        help="Override autodetected commit hash for this application [$SCOPE_COMMIT_SHA]")
    parser.add_argument("--repository", "-r", type=str, required=False, default=os.getenv('SCOPE_REPOSITORY'),
                        dest='repository',
                        help="Override autodetected repository URL for this application [$SCOPE_REPOSITORY]")
    parser.add_argument("--root", type=str, required=False, default=os.getenv('SCOPE_SOURCE_ROOT'), dest='root',
                        help="Override autodetected repository root path for this application "
                             "[$SCOPE_SOURCE_ROOT]")
    parser.add_argument("--debug", "-D", action='store_true', default=os.getenv('SCOPE_DEBUG'), dest='debug',
                        help="Log debugging information to the console [$SCOPE_DEBUG]")
    parser.add_argument("--dry-run", action='store_true', default=os.getenv('SCOPE_DRYRUN'), dest='dryrun',
                        help=argparse.SUPPRESS)
    parser.add_argument("--version", "-v", action='store_true', dest='version',
                        help="Print version information and exit")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="command to run")
    args = parser.parse_args()

    if args.version:
        print(version)
        exit(0)

    if not args.command:
        parser.print_help()
        exit(1)

    if args.debug:
        os.environ['SCOPE_DEBUG'] = '1'
        logging.basicConfig()
        logging.getLogger('scopeagent').setLevel(logging.DEBUG)

    if args.dryrun:
        os.environ['SCOPE_DRYRUN'] = '1'

    git_info = autodetect_git_info()
    commit = args.commit or git_info.get('commit')
    if not commit:
        print("Couldn't autodetect commit and $SCOPE_COMMIT_SHA wasn't provided")
        exit(1)
    os.environ['SCOPE_COMMIT_SHA'] = commit

    repository = args.repository or git_info.get('repository')
    if not repository:
        print("Couldn't autodetect repository ID and $SCOPE_REPOSITORY wasn't provided")
        exit(1)
    os.environ['SCOPE_REPOSITORY'] = repository

    os.environ['SCOPE_SOURCE_ROOT'] = args.root or git_info.get('root') or os.getcwd()

    if not args.apikey:
        print("API key is required, either as an environment variable ($SCOPE_APIKEY) or as an argument (-k)")
        exit(1)
    os.environ['SCOPE_APIKEY'] = args.apikey

    if not args.api_endpoint:
        print("API endpoint is required, either as an environment variable ($SCOPE_API_ENDPOINT) "
              "or as an argument (-e)")
        exit(1)
    os.environ['SCOPE_API_ENDPOINT'] = args.api_endpoint

    if args.name:
        os.environ['SCOPE_SERVICE'] = args.name

    os.environ['SCOPE_COMMAND'] = " ".join(args.command)

    run(args.command)


def run(command):
    from .wrapper import __file__ as file
    wrapper_path = os.path.dirname(file)
    from ..vendor import __file__ as file
    vendor_path = os.path.dirname(file)

    paths = "%s%s%s" % (wrapper_path, os.path.pathsep, vendor_path)

    if os.environ.get('PYTHONPATH'):
        os.environ['PYTHONPATH'] = "%s%s%s" % (paths, os.path.pathsep, os.environ['PYTHONPATH'])
    else:
        os.environ['PYTHONPATH'] = paths
    os.execvp(command[0], command)


def autodetect_git_info():
    info = {}
    try:
        info['commit'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], stderr=subprocess.STDOUT)\
            .decode('utf-8').strip()
        info['root'] = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], stderr=subprocess.STDOUT)\
            .decode('utf-8').strip()
        info['repository'] = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], stderr=subprocess.STDOUT) \
            .decode('utf-8').strip()
    except (FileNotFoundError, subprocess.CalledProcessError,):
        logger.debug("couldn't autodetect git information", exc_info=True)
    logger.debug("autodetected git info: %s", info)
    return info
