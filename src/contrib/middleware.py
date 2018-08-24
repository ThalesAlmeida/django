# -*- coding: utf-8 -*-
# from contrib.utils import getLogger
import logging

try:
    from threading import local
except ImportError:
    # from django.utils._threading_local import local, Thread
    logger = logging.getLogger(__name__)

_thread_locals = local()


def get_current_user():
    return getattr(_thread_locals, 'user', None)
