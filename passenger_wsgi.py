import os, sys
sys.path.insert(0, '/home/c/clickoff/clickoff.beget.tech/project')
sys.path.insert(1, '/home/c/clickoff/.local/lib/python3.9/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()