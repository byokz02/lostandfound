"""
WSGI config for lost_found_school project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# This directory (inner lost_found_school/ with __init__.py, urls.py, settings.py)
INNER_PACKAGE_DIR = Path(__file__).resolve().parent

# Django project root (parent of items/ and lost_found_school/)
PROJECT_ROOT = INNER_PACKAGE_DIR.parent

# Ensure the project root is on sys.path so 'items' is importable
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Fix: The outer lost_found_school/ directory (no __init__.py) may be imported
# as a namespace package, causing its __path__ to point to the wrong directory.
# Correct __path__ to point to this inner directory where urls.py etc. actually live.
import lost_found_school
lost_found_school.__path__ = [str(INNER_PACKAGE_DIR)]

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lost_found_school.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
