# app_name/__init__.py

from django.apps import AppConfig

class AppNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_name'

    def ready(self):
        from django.template import engines
        from .filters import jinja2_range

        jinja_engine = engines['jinja2']
        jinja_engine.filters['range'] = jinja2_range
