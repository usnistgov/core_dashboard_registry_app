"""
    Common views
"""
from core_dashboard_common_app.views.common.views import DashboardRecords
from core_dashboard_common_app.views.user.views import DashboardWorkspaceRecords
from core_dashboard_registry_app import constants as dashboard_constants
from core_dashboard_registry_app.settings import INSTALLED_APPS
from core_main_app.components.user import api as user_api
from core_main_app.components.user.api import get_id_username_dict
from core_main_app.utils.rendering import render
from core_main_registry_app.commons.constants import DataStatus
from core_main_registry_app.components.data.api import get_status
from core_main_app.components.workspace import api as workspace_api


def home(request):
    """ Home page.

    Args:
        request:

    Returns:
    """

    context = {}
    if 'core_curate_app' in INSTALLED_APPS:
        context.update({'draft': True})

    assets = {
        "css": ['core_dashboard_registry_app/user/css/home.css'],
    }

    return render(request, dashboard_constants.DASHBOARD_HOME_TEMPLATE, context=context,
                  assets=assets)


class DashboardRegistryRecords(DashboardRecords):
    """ List the records for the registry
    """

    def _format_data_context(self, data_list):
        data_context_list = []
        username_list = dict((str(x.id), x.username) for x in user_api.get_all_users())
        for data in data_list:
            data_context_list.append({'data': data,
                                      'username_list': username_list,
                                      'data_status': get_status(data),
                                      'data_status_values': DataStatus,
                                      'can_read': True,
                                      'can_write': True,
                                      'is_owner': True,
                                      'can_change_workspace': self.can_change_workspace(data),
                                      'can_set_public': not (data.workspace is not None and workspace_api.is_workspace_public(data.workspace))
                                      })
        return data_context_list

    def _get_assets(self):
        # add js & css for the super class
        assets = super(DashboardRegistryRecords, self)._get_assets()
        # add css relatives to the registry
        assets['css'].append("core_dashboard_registry_app/user/css/list/records.css")
        # add js relatives to the registry
        assets['js'].append({
            "path": 'core_dashboard_registry_app/user/js/list/records.js',
            "is_raw": False
        })
        assets['js'].append({
            "path": 'core_dashboard_registry_app/user/js/list/records.raw.js',
            "is_raw": True
        })
        assets['js'].append({
            "path": dashboard_constants.JS_PUBLISH_RESOURCE,
            "is_raw": False
        })
        return assets


class DashboardRegistryWorkspaceRecords(DashboardWorkspaceRecords):
    """ List the records of a workspace for the registry.
    """

    def _format_data_context(self, data_list, user, user_can_read, user_can_write):
        detailed_user_data = []
        username_list = get_id_username_dict(user_api.get_all_users())
        for data in data_list:
            is_owner = str(data.user_id) == str(user.id)
            detailed_user_data.append({'data': data,
                                       'username_list': username_list,
                                       'data_status': get_status(data),
                                       'data_status_values': DataStatus,
                                       'can_read': user_can_read or is_owner,
                                       'can_write': user_can_write or is_owner,
                                       'is_owner': is_owner})
        return detailed_user_data

    def _get_assets(self):
        # add js & css for the super class
        assets = super(DashboardRegistryWorkspaceRecords, self)._get_assets()
        # add css relatives to the registry
        assets['css'].append("core_dashboard_registry_app/user/css/list/records.css")
        # add js relatives to the registry
        assets['js'].append({
            "path": 'core_dashboard_registry_app/user/js/list/records.js',
            "is_raw": False
        })
        assets['js'].append({
            "path": 'core_dashboard_registry_app/user/js/list/records.raw.js',
            "is_raw": True
        })
        return assets
