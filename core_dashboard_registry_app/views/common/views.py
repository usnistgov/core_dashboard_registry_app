""" Common views for the registry dashboard
"""
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.urls import reverse_lazy

import core_curate_app.components.curate_data_structure.api as curate_data_structure_api
from core_dashboard_common_app import constants as dashboard_common_constants
from core_dashboard_common_app import settings
from core_dashboard_common_app.views.common.forms import ActionForm, UserForm
from core_dashboard_common_app.views.common.views import (
    DashboardRecords,
    DashboardForms,
)
from core_dashboard_common_app.views.common.views import DashboardWorkspaceRecords
from core_dashboard_registry_app import constants as dashboard_constants
from core_dashboard_registry_app.settings import INSTALLED_APPS
from core_dashboard_registry_app.utils.query.mongo.prepare import (
    create_query_dashboard_resources,
)
from core_dashboard_registry_app.views.common.ajax import EditDataView
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions as exceptions
from core_main_app.components.data import api as data_api
from core_main_app.components.user import api as user_api
from core_main_app.components.user.api import get_id_username_dict
from core_main_app.components.workspace.api import check_if_workspace_can_be_changed
from core_main_app.utils.pagination.django_paginator.results_paginator import (
    ResultsPaginator,
)
from core_main_app.utils.rendering import render
from core_main_registry_app.commons.constants import DataStatus
from core_main_registry_app.components.custom_resource import api as custom_resource_api
from core_main_registry_app.components.data.api import get_status, get_role
from core_main_registry_app.constants import CUSTOM_RESOURCE_TYPE
from core_main_registry_app.settings import ENABLE_BLOB_ENDPOINTS

if "core_curate_registry_app" in INSTALLED_APPS:
    import core_curate_registry_app.components.curate_data_structure.api as curate_data_structure_registry_api


@login_required(login_url=reverse_lazy("core_main_app_login"))
def home(request):
    """Home page.

    Args:
        request:

    Returns:
    """

    context = {}
    if "core_curate_app" in INSTALLED_APPS:
        context.update({"draft": True})

    if ENABLE_BLOB_ENDPOINTS:
        context.update({"show_blob_menu": True})

    assets = {
        "css": ["core_dashboard_registry_app/user/css/home.css"],
    }

    return render(
        request,
        dashboard_constants.DASHBOARD_HOME_TEMPLATE,
        context=context,
        assets=assets,
    )


class DashboardRegistryRecords(DashboardRecords):
    """List the records for the registry"""

    def _get_list_name_in_shema_from_slug(self, role_name_list, custom_resources):
        """Get list of name in schema for each role in request

        Args:
            role_name_list:
            custom_resources:
        Returns:
        """
        list_name_in_schema = []
        for role in role_name_list:
            for custom_resource in custom_resources:
                if custom_resource.slug == role:
                    list_name_in_schema.append(custom_resource.name_in_schema)

        return list_name_in_schema

    def load_records(self, request, is_published, custom_resources):
        """Get list of records

        Args:
            request:
            is_published:
            custom_resources:
        Returns:
            filtered_data
        """
        role_name_list = self._get_list_name_in_shema_from_slug(
            request.GET.getlist("role", []), custom_resources
        )
        filtered_data = []
        try:
            loaded_data = data_api.execute_json_query(
                create_query_dashboard_resources(
                    request, role_name_list, self.administration
                ),
                request.user,
            )
        except AccessControlError:
            loaded_data = []
        for data in loaded_data:
            if (
                is_published is None
                or (is_published == "true" and data_api.is_data_public(data))
                or (is_published == "false" and not data_api.is_data_public(data))
            ):
                filtered_data.append(data)
        return filtered_data

    def load_drafts(self, request, context):
        """Get list of drafts

        Args:
            request:
            context:
        Returns:
            filtered_data
        """

        role_name_list = request.GET.getlist("role", [])
        filtered_data = []

        if self.administration:
            forms = curate_data_structure_api.get_all_with_no_data(request.user)
        else:
            forms = curate_data_structure_api.get_all_by_user_id_with_no_data(
                request.user.id
            )

        detailed_forms = []
        for form in forms:
            try:
                role = ", ".join(
                    [
                        custom_resource_api.get_by_role_for_current_template(
                            x, request=request
                        ).title
                        for x in curate_data_structure_registry_api.get_role(form)
                    ]
                    if form.form_string
                    else ["None"]
                )
            except exceptions.ModelError:
                role = "None"
            if role_name_list != []:
                if "-".join(role.lower().split()) in context["roles"]:
                    detailed_forms.append({"form": form, "role": role})
            else:
                detailed_forms.append({"form": form, "role": role})
        filtered_data.extend(detailed_forms)
        return filtered_data

    def get(self, request, *args, **kwargs):
        """Retrieve a list of drafts or records

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: Data
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """

        # TODO: use custom_resource to get cr_type_all
        cr_type_all = custom_resource_api.get_current_custom_resource_type_all(
            request=request
        )

        custom_resources = list(
            custom_resource_api.get_all_of_current_template(request=request).order_by(
                "sort"
            )
        )
        # Get arguments

        is_published = request.GET.get("ispublished", None)
        is_published = (
            None if is_published not in ["true", "false", "draft"] else is_published
        )
        page = request.GET.get("page", 1)
        if is_published == "draft":
            document = dashboard_common_constants.FUNCTIONAL_OBJECT_ENUM.FORM.value
            template = dashboard_constants.DASHBOARD_FORMS_TEMPLATE_TABLE_PAGINATION
        else:
            document = dashboard_common_constants.FUNCTIONAL_OBJECT_ENUM.RECORD.value
            template = self.data_template

        context = {
            "page": page,
            "roles": ",".join(request.GET.getlist("role", [cr_type_all.slug])),
            "ispublished": is_published,
        }

        # Get resources
        if is_published == "draft":
            filtered_data = self.load_drafts(request, context)
        else:
            filtered_data = self.load_records(request, is_published, custom_resources)

        # Paginator
        results_paginator = ResultsPaginator.get_results(
            filtered_data, page, settings.RECORD_PER_PAGE_PAGINATION
        )

        # Data context
        if is_published != "draft":
            results_paginator.object_list = self._format_data_context_registry(
                results_paginator.object_list, is_published
            )

        # Add user_form for change owner
        user_form = UserForm(request.user)
        context.update(
            {
                "number_total": len(filtered_data),
                "user_data": results_paginator,
                "user_form": user_form,
                "document": document,
                "template": template,
                "action_form": ActionForm([("2", "Change owner of selected records")]),
                "menu": self.administration,
                "administration": self.administration,
                "username_list": get_id_username_dict(user_api.get_all_users()),
                "resources": True,
                "url_resources": reverse("core-admin:core_dashboard_records")
                if self.administration
                else reverse("core_dashboard_records"),
                "custom_resources": custom_resources,
                "display_not_resource": True,  # display all resource
                "role_custom_resource_type_all": cr_type_all.slug,
                "list_role_custom_resource": ",".join(
                    [
                        cr.slug
                        for cr in custom_resources
                        if custom_resource_api._is_custom_resource_type_resource(cr)
                        and cr.display_icon
                    ]
                ),
                "type_resource": CUSTOM_RESOURCE_TYPE.RESOURCE.value,
            }
        )

        modals = [
            "core_main_app/user/workspaces/list/modals/assign_workspace.html",
            dashboard_common_constants.MODALS_COMMON_DELETE,
            dashboard_common_constants.MODALS_COMMON_CHANGE_OWNER,
            EditDataView.get_modal_html_path(),
        ]

        assets = self._get_assets()

        return self.common_render(
            request, self.template, context=context, assets=assets, modals=modals
        )

    # FIXME is_published is never used
    def _format_data_context_registry(self, data_list, is_published):
        data_context_list = []
        username_list = dict((x.id, x.username) for x in user_api.get_all_users())
        for data in data_list:
            data_context_list.append(
                {
                    "data": data,
                    "username_list": username_list,
                    "data_status": get_status(data),
                    "data_status_values": DataStatus,
                    "data_role": ", ".join(
                        [
                            _get_role_label(x, request=self.request)
                            for x in get_role(data)
                        ]
                    ),
                    "can_read": True,
                    "can_write": True,
                    "is_owner": True,
                    "can_change_workspace": check_if_workspace_can_be_changed(data),
                    "can_set_public": not data_api.is_data_public(data),
                }
            )
        return data_context_list

    def _get_assets(self):
        # add js & css for the super class
        assets = super()._get_assets()
        # add css relatives to the registry
        assets["css"].append("core_dashboard_registry_app/user/css/list/records.css")
        assets["css"].append(
            "core_main_registry_app/user/css/resource_banner/resource_banner.css"
        )
        assets["css"].append(dashboard_constants.CSS_SELECTION)
        # add js relatives to the registry
        assets["js"].append(
            {
                "path": "core_dashboard_registry_app/user/js/list/records.js",
                "is_raw": False,
            }
        )
        assets["js"].append(
            {
                "path": "core_dashboard_registry_app/user/js/list/records.raw.js",
                "is_raw": True,
            }
        )
        assets["js"].append(
            {"path": dashboard_constants.JS_PUBLISH_RESOURCE, "is_raw": False}
        )
        assets["js"].append(
            {"path": dashboard_constants.JS_RECORD_REGISTRY, "is_raw": False}
        )
        assets["js"].append(
            {"path": "core_dashboard_registry_app/user/js/get_url.js", "is_raw": False}
        )
        assets["js"].append(EditDataView.get_modal_js_path())
        return assets


class DashboardRegistryWorkspaceRecords(DashboardWorkspaceRecords):
    """List the records of a workspace for the registry."""

    def _format_data_context(self, data_list, user, user_can_read, user_can_write):
        detailed_user_data = []
        username_list = get_id_username_dict(user_api.get_all_users())
        for data in data_list:
            is_owner = str(data.user_id) == str(user.id) or self.administration
            detailed_user_data.append(
                {
                    "data": data,
                    "username_list": username_list,
                    "data_status": get_status(data),
                    "data_status_values": DataStatus,
                    "data_role": ", ".join(
                        [
                            _get_role_label(x, request=self.request)
                            for x in get_role(data)
                        ]
                    ),
                    "can_read": user_can_read or is_owner,
                    "can_write": user_can_write or is_owner,
                    "is_owner": is_owner,
                }
            )
        return detailed_user_data

    def _get_modals(self):
        modals = super()._get_modals()
        modals.append(EditDataView.get_modal_html_path())
        return modals

    def _get_assets(self):
        # add js & css for the super class
        assets = super()._get_assets()
        # add css relatives to the registry
        assets["css"].append("core_dashboard_registry_app/user/css/list/records.css")
        # add js relatives to the registry
        assets["js"].append(
            {
                "path": "core_dashboard_registry_app/user/js/list/records.js",
                "is_raw": False,
            }
        )
        assets["js"].append(
            {
                "path": "core_dashboard_registry_app/user/js/list/records.raw.js",
                "is_raw": True,
            }
        )
        assets["js"].append(
            {"path": "core_dashboard_registry_app/user/js/get_url.js", "is_raw": False}
        )
        assets["js"].append(EditDataView.get_modal_js_path())
        return assets


class DashboardRegistryForms(DashboardForms):
    """List the forms."""

    def _get_detailed_forms(self, forms):
        detailed_forms = []
        for form in forms:
            try:
                role = ", ".join(
                    [
                        custom_resource_api.get_by_role_for_current_template(
                            x, request=self.request
                        ).title
                        for x in curate_data_structure_registry_api.get_role(form)
                    ]
                    if form.form_string
                    else ["None"]
                )
            except exceptions.ModelError:
                role = "None"

            detailed_forms.append({"form": form, "role": role})
        return detailed_forms


def _get_role_label(role, request):
    """Get role label

    Get role label from custom resources if found, get it from xsd otherwise

    Args:
        role:

    Returns:

    """
    try:
        return custom_resource_api.get_by_role_for_current_template(
            role, request=request
        ).title
    except (exceptions.ModelError, exceptions.DoesNotExist):
        return role
