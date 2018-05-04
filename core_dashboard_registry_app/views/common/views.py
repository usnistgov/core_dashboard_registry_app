"""
    Common views
"""

from core_main_app.utils.rendering import render
from core_dashboard_registry_app import constants as dashboard_constants
from core_dashboard_registry_app.settings import INSTALLED_APPS


def home(request):
    """ Home page.

    Args:
        request:

    Returns:
    """

    context = {}
    if 'core_curate_app' in INSTALLED_APPS:
        context.update({'draft': True})

    return render(request, dashboard_constants.DASHBOARD_HOME_TEMPLATE, context=context)
