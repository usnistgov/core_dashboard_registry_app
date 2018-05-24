"""
    Django settings for core_dashboard_registry_app app
"""
from django.conf import settings

if not settings.configured:
    settings.configure()

SERVER_URI = getattr(settings, 'SERVER_URI', "http://localhost")

INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])

DATA_DISPLAY_NAME = getattr(settings, 'DATA_DISPLAY_NAME', 'resource')
DRAFT_DISPLAY_NAME = getattr(settings, 'DRAFT_DISPLAY_NAME', 'draft')
WORKSPACE_DISPLAY_NAME = getattr(settings, 'WORKSPACE_DISPLAY_NAME', 'workspace')
