import os, sys
from os.path import abspath, dirname, join

#path = '/home/wilblack/django-projects'
path = abspath(join(dirname(__file__), "../../"))

if path not in sys.path:
    sys.path.append(path)

path = abspath(join(dirname(__file__), "../"))
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'kegtv2.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
