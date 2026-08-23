import os
from dotenv import load_dotenv
from django.core.asgi import get_asgi_application

# Must run before the setdefault below — see manage.py for why.
load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.development")
application = get_asgi_application()
