"""
WSGI config for mirri_validator_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import sys

sys.path.append("/home/peio/devel/cect/mirri_utils")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mirri_tools_web.settings")

application = get_wsgi_application()
