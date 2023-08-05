import logging
import os
import platform
import uuid
from os.path import basename

try:
    from queue import Queue
except ImportError:
    from Queue import Queue

import opentracing

import scopeagent
from ..instrumentation import patch_all
from ..tracer import BasicTracer, tags
from ..recorders.http import HTTPRecorder

logger = logging.getLogger(__name__)


class Agent:
    def __init__(self, api_key, api_endpoint, repository=None, commit=None, source_root=None, service=None,
                 debug=False, command=None, dry_run=False):
        if debug:
            logging.basicConfig()
            logging.getLogger('scopeagent').setLevel(logging.DEBUG)
        self.dry_run = dry_run
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.repository = \
            repository or \
            os.getenv('SCOPE_REPOSITORY') or \
            os.getenv('GIT_URL') or \
            os.getenv('CIRCLE_REPOSITORY_URL') or \
            ("https://github.com/%s.git" % os.getenv('TRAVIS_REPO_SLUG') if os.getenv('TRAVIS_REPO_SLUG') else None) or\
            os.getenv('CI_REPOSITORY_URL')
        self.commit = \
            commit or \
            os.getenv('SCOPE_COMMIT_SHA') or \
            os.getenv('GIT_COMMIT') or \
            os.getenv('CIRCLE_SHA1') or \
            os.getenv('TRAVIS_COMMIT') or \
            os.getenv('CI_COMMIT_SHA')
        self.source_root = \
            source_root or \
            os.getenv('SCOPE_SOURCE_ROOT') or \
            os.getenv('WORKSPACE') or \
            os.getenv('CIRCLE_WORKING_DIRECTORY') or \
            os.getenv('TRAVIS_BUILD_DIR') or \
            os.getenv('CI_PROJECT_DIR')
        self.service = service or 'default'
        self.tracer = None
        self.in_live_test = False
        self._functions = {}
        self.command = command
        self.hostname = platform.node()
        self.agent_id = str(uuid.uuid4())

    def get_default_service_name(self):
        return basename(self.source_root)

    def install(self):
        # Install tracer
        metadata = {
            tags.AGENT_ID: self.agent_id,
            tags.AGENT_VERSION: scopeagent.version,
            tags.SERVICE: self.service,
            tags.REPOSITORY: self.repository,
            tags.COMMIT: self.commit,
            tags.HOSTNAME: self.hostname,
            tags.COMMAND: self.command,
            tags.SOURCE_ROOT: self.source_root,
            tags.PLATFORM_NAME: platform.system(),
            tags.PLATFORM_VERSION: platform.release(),
            tags.ARCHITECTURE: platform.machine(),
            tags.PYTHON_IMPLEMENTATION: platform.python_implementation(),
            tags.PYTHON_VERSION: platform.python_version(),
        }
        metadata.update(get_ci_tags())
        logger.debug("metadata=%s", metadata)

        recorder = HTTPRecorder(test_only=True, api_key=self.api_key, api_endpoint=self.api_endpoint, metadata=metadata)
        self.tracer = BasicTracer(recorder)
        scopeagent.global_agent = self
        opentracing.tracer = self.tracer

        # Patch all supported libraries
        patch_all()


def get_ci_tags():
    if os.getenv('TRAVIS'):
        return {
            tags.CI: True,
            tags.CI_PROVIDER: 'Travis',
            tags.CI_BUILD_ID: os.getenv('TRAVIS_BUILD_ID'),
            tags.CI_BUILD_NUMBER: os.getenv('TRAVIS_BUILD_NUMBER'),
            tags.CI_BUILD_URL: "https://travis-ci.com/%s/builds/%s" % (os.getenv('TRAVIS_REPO_SLUG'),
                                                                       os.getenv('TRAVIS_BUILD_ID')),
        }
    elif os.getenv('CIRCLECI'):
        return {
            tags.CI: True,
            tags.CI_PROVIDER: 'CircleCI',
            tags.CI_BUILD_NUMBER: os.getenv('CIRCLE_BUILD_NUM'),
            tags.CI_BUILD_URL: os.getenv('CIRCLE_BUILD_URL'),
        }
    elif os.getenv('JENKINS_URL'):
        return {
            tags.CI: True,
            tags.CI_PROVIDER: 'Jenkins',
            tags.CI_BUILD_ID: os.getenv('BUILD_ID'),
            tags.CI_BUILD_NUMBER: os.getenv('BUILD_NUMBER'),
            tags.CI_BUILD_URL: os.getenv('BUILD_URL'),
        }
    elif os.getenv('GITLAB_CI'):
        return {
            tags.CI: True,
            tags.CI_PROVIDER: 'GitLab',
            tags.CI_BUILD_ID: os.getenv('CI_JOB_ID'),
            tags.CI_BUILD_URL: os.getenv('CI_JOB_URL'),
        }
    else:
        return {
            tags.CI: False
        }
