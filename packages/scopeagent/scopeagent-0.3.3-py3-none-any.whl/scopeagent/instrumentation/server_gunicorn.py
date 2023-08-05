import logging

import wrapt

from .wrappers.wsgi import wrap_wsgi


logger = logging.getLogger(__name__)


def wrapper(wrapped, instance, args, kwargs):
    return wrap_wsgi(wrapped(*args, **kwargs))


def patch():
    try:
        logger.debug("patching module=gunicorn.app.base name=Application.wsgi")
        wrapt.wrap_function_wrapper('gunicorn.app.base', 'Application.wsgi', wrapper)
    except ImportError:
        logger.debug("module not found module=gunicorn.app.base")
