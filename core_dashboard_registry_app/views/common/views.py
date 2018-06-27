"""
    Common views
"""
from django.core.urlresolvers import reverse

from core_dashboard_common_app import constants as dashboard_common_constants
from core_dashboard_common_app import settings
from core_dashboard_common_app.views.common.forms import ActionForm, UserForm
from core_dashboard_common_app.views.common.views import DashboardRecords
from core_dashboard_common_app.views.user.views import DashboardWorkspaceRecords
from core_dashboard_registry_app import constants as dashboard_constants
from core_dashboard_registry_app.settings import INSTALLED_APPS
from core_dashboard_registry_app.utils.query.mongo.prepare import create_query_dashboard_resources
from core_main_app.components.data import api as data_api
from core_main_app.components.user import api as user_api
from core_main_app.components.user.api import get_id_username_dict
from core_main_app.utils.access_control.exceptions import AccessControlError
from core_main_app.utils.pagination.django_paginator.results_paginator import ResultsPaginator
from core_main_app.utils.rendering import render
from core_main_registry_app.commons.constants import DataStatus, DataRole
from core_main_registry_app.components.data.api import get_status, get_role


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

    def get(self, request, *args, **kwargs):

        # Get arguments
        is_published = request.GET.get('ispublished', None)
        role_name_list = request.GET.getlist('role', ['all'])
        page = request.GET.get('page', 1)

        role_name = ','.join(role_name_list)

        context = {'page': page,
                   'roles': role_name,
                   'ispublished': is_published}

        # Get resources
        try:
            loaded_data = data_api.execute_query(create_query_dashboard_resources(request,
                                                                                  role_name_list,
                                                                                  self.administration),
                                                 request.user, '-last_modification_date')
        except AccessControlError, ace:
            loaded_data = []

        # Filter publish/not published data
        filtered_data = []
        for data in loaded_data:
            if (is_published is None or (is_published == 'true' and data_api.is_data_public(data)) or
                    (is_published == 'false' and not data_api.is_data_public(data))):
                filtered_data.append(data)

        # Paginator
        results_paginator = ResultsPaginator.get_results(filtered_data, page, settings.RECORD_PER_PAGE_PAGINATION)

        # Data context
        results_paginator.object_list = self._format_data_context_registry(results_paginator.object_list, is_published)

        # Add user_form for change owner
        user_form = UserForm(request.user)
        context.update({
            'other_users_data': results_paginator,
            'user_form': user_form,
            'document': self.document,
            'template': self.data_template,
            'action_form': ActionForm([('1', 'Delete selected records'),
                                       ('2', 'Change owner of selected records')]),
            'menu': self.administration,
            'administration': self.administration,
            'username_list': get_id_username_dict(user_api.get_all_users()),
            'resources' : True,
            'url_resources': reverse('admin:core_dashboard_records') if self.administration else
            reverse('core_dashboard_records')
        })

        modals = ["core_main_app/user/workspaces/list/modals/assign_workspace.html",
                  dashboard_common_constants.MODALS_COMMON_DELETE,
                  dashboard_common_constants.MODALS_COMMON_CHANGE_OWNER
                  ]

        assets = self._get_assets()

        return self.common_render(request, self.template,
                                  context=context,
                                  assets=assets,
                                  modals=modals)

    def _format_data_context_registry(self, data_list, is_published):
        data_context_list = []
        username_list = dict((str(x.id), x.username) for x in user_api.get_all_users())
        for data in data_list:
            data_context_list.append({'data': data,
                                      'username_list': username_list,
                                      'data_status': get_status(data),
                                      'data_status_values': DataStatus,
                                      'data_role': ', '.join([DataRole.role[x] for x in get_role(data)]),
                                      'can_read': True,
                                      'can_write': True,
                                      'is_owner': True,
                                      'can_change_workspace': self.can_change_workspace(data),
                                      'can_set_public': not data_api.is_data_public(data)
                                      })
        return data_context_list

    def _get_assets(self):
        # add js & css for the super class
        assets = super(DashboardRegistryRecords, self)._get_assets()
        # add css relatives to the registry
        assets['css'].append("core_dashboard_registry_app/user/css/list/records.css")
        assets['css'].append(dashboard_constants.CSS_SELECTION)
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
        assets['js'].append({
            "path": dashboard_constants.JS_RECORD_REGISTRY,
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
                                       'data_role': ', '.join([DataRole.role[x] for x in get_role(data)]),
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
