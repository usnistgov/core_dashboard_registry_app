"""
    Django settings for core_dashboard_registry_app app
"""

from django.conf import settings

if not settings.configured:
    settings.configure()

SERVER_URI = getattr(settings, 'SERVER_URI', "http://localhost")

INSTALLED_APPS = getattr(settings, 'INSTALLED_APPS', [])

menu = {
    'Records': ('core_dashboard_records', 2000),
    'Workspaces': ('core_dashboard_workspaces', 4000),
}

if 'core_curate_app' in INSTALLED_APPS:
    menu['Forms'] = ('core_dashboard_forms', 2500)

# Menu
DASHBOARD_MENU = getattr(settings, 'DASHBOARD_MENU', menu)
