"""
    Django settings for core_dashboard_registry_app app
"""

from django.conf import settings

from core_dashboard_registry_app.constants import FUNCTIONAL_OBJECT_ENUM

if not settings.configured:
    settings.configure()

SERVER_URI = getattr(settings, 'SERVER_URI', "http://localhost")

INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])

menu = {
    '{0}s'.format(FUNCTIONAL_OBJECT_ENUM.RESOURCE.title()): ('core_dashboard_records', 2000),
    '{0}s'.format(FUNCTIONAL_OBJECT_ENUM.WORKSPACE.title()): ('core_dashboard_workspaces', 4000),
}

if 'core_curate_app' in INSTALLED_APPS:
    menu['{0}s'.format(FUNCTIONAL_OBJECT_ENUM.DRAFT.title())] = ('core_dashboard_forms', 2500)

# Menu
DASHBOARD_MENU = getattr(settings, 'DASHBOARD_MENU', menu)
