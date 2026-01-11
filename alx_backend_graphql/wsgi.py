"""
<<<<<<< HEAD
WSGI config for alx_backend_graphql project.
=======
WSGI config for alx_backend_graphql_crm project.
>>>>>>> 74fab26 (Scheduling and Automating Tasks)

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
<<<<<<< HEAD
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
=======
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
>>>>>>> 74fab26 (Scheduling and Automating Tasks)
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')

application = get_wsgi_application()
