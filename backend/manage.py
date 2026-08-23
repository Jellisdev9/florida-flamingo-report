#!/usr/bin/env python
import os
import sys

from dotenv import load_dotenv


def main():
    # Must run before the setdefault below — otherwise DJANGO_SETTINGS_MODULE
    # from .env can never override the development default, since
    # backend/settings/base.py's own load_dotenv() call only runs after
    # a settings module has already been chosen.
    load_dotenv()
    # `test` always runs against backend.settings.test regardless of
    # .env's DJANGO_SETTINGS_MODULE — production.py's SECURE_SSL_REDIRECT
    # would 301 every request the test client makes, since it only speaks
    # plain HTTP.
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings.test"
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.development")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
