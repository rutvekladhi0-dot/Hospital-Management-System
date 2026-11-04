"""
WSGI config for medcare project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medcare.settings')
application = get_wsgi_application()
