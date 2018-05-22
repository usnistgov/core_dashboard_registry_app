"""
    Registry User Dashboard constants
"""
from core_dashboard_common_app.utils.enum import enum

# Templates
DASHBOARD_HOME_TEMPLATE = 'core_dashboard_registry_app/home.html'

FUNCTIONAL_OBJECT_ENUM = enum(RESOURCE='resource',
                              DRAFT='draft',
                              WORKSPACE='workspace')
