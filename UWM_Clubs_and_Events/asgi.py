"""
ASGI config for UWM_Clubs_and_Events project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UWM_Clubs_and_Events.settings')

application = get_asgi_application()
