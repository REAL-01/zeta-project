import os
import sys

# Абсолютный путь к проекту на хостинге
project_path = '/var/www/u3481426/data/www/zeta-strategy.ru'
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Путь к виртуальному окружению
venv_path = os.path.join(project_path, 'venv/lib/python3.10/site-packages')
if venv_path not in sys.path:
    sys.path.insert(1, venv_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'zeta_web.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
