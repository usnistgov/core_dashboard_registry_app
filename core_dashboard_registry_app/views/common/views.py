""" Common views for the registry dashboard
"""
from django.conf import settings as conf_settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator

import core_curate_app.components.curate_data_structure.api as curate_data_structure_api
from core_dashboard_common_app import constants as dashboard_common_constants
from core_dashboard_common_app import settings
from core_dashboard_common_app.views.common.forms import ActionForm, UserForm
from core_dashboard_common_app.views.common.views import (
    DashboardRecords,
    DashboardForms,
)
from core_dashboard_common_app.views.common.views import (
    DashboardWorkspaceRecords,
)
from core_dashboard_registry_app import constants as dashboard_constants
from core_dashboard_registry_app.settings import INSTALLED_APPS
from core_dashboard_registry_app.utils.query.mongo.prepare import (
    create_query_dashboard_resources,
    create_query_other_resources,
)
from core_dashboard_registry_app.views.common.ajax import EditDataView
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions as exceptions
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.data import api as data_api
from core_main_app.components.user import api as user_api
from core_main_app.components.user.api import get_id_username_dict
from core_main_app.components.workspace import api as workspace_api
from core_main_app.components.workspace.api import (
    check_if_workspace_can_be_changed,
)
from core_main_app.utils.pagination.django_paginator.results_paginator import (
    ResultsPaginator,
)
from core_main_app.utils.rendering import render
from core_main_registry_app.commons.constants import DataStatus
from core_main_registry_app.components.custom_resource import (
    api as custom_resource_api,
)
from core_main_registry_app.components.data.api import get_status, get_role
from core_main_registry_app.constants import CUSTOM_RESOURCE_TYPE
from core_main_registry_app.settings import (
    ENABLE_BLOB_ENDPOINTS,
    ALLOW_MULTIPLE_SCHEMAS,
)

if "core_curate_registry_app" in INSTALLED_APPS:
    import core_curate_registry_app.components.curate_data_structure.api as curate_data_structure_registry_api


@login_required
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

    # Set page title
    context.update({"page_title": "Dashboard"})

    return render(
        request,
        dashboard_constants.DASHBOARD_HOME_TEMPLATE,
        context=context,
        assets=assets,
    )


@method_decorator(login_required, name="dispatch")
class DashboardRegistryRecords(DashboardRecords):
    """List the records for the registry"""

    def _get_list_name_in_shema_from_slug(
        self, role_name_list, custom_resources
    ):
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

    def load_records(self, request, tab, custom_resources):
        """Get list of records

        Args:
            request:
            tab:
            custom_resources:
        Returns:
            filtered_data
        """
        role_name_list = self._get_list_name_in_shema_from_slug(
            request.GET.getlist("role", []), custom_resources
        )
        try:
            if conf_settings.MONGODB_INDEXING:
                from mongoengine.queryset.visitor import Q
                from core_main_app.components.mongo.api import (
                    execute_mongo_query,
                )

                workspace_key = "_workspace_id"
                query_api = execute_mongo_query
            else:
                from mongoengine.queryset.visitor import Q
                from core_main_app.components.data.api import execute_query

                workspace_key = "workspace_id"
                query_api = execute_query

            loaded_data = query_api(
                create_query_dashboard_resources(
                    request, role_name_list, self.administration
                ),
                request.user,
            )
        except AccessControlError:
            return []

        if tab == "published":
            global_workspace = workspace_api.get_global_workspace()
            filtered_data = loaded_data.filter(
                Q(**{f"{workspace_key}": global_workspace.id})
            )
        elif tab == "unpublished":
            filtered_data = loaded_data.filter(Q(**{f"{workspace_key}": None}))
        else:
            filtered_data = loaded_data

        return filtered_data

    def load_other_records(self, request):
        """Get list of records not curated using registry template

        Args:
            request:

        Returns:
            filtered_data
        """
        try:
            if conf_settings.MONGODB_INDEXING:
                from core_main_app.components.mongo.api import (
                    execute_mongo_query,
                )

                query_api = execute_mongo_query
            else:
                from core_main_app.components.data.api import execute_query

                query_api = execute_query

            loaded_data = query_api(
                create_query_other_resources(request, self.administration),
                request.user,
            )
        except AccessControlError:
            return []

        return loaded_data

    def load_drafts(self, request):
        """Get list of drafts

        Args:
            request:
        Returns:
            filtered_data
        """
        if self.administration:
            forms = curate_data_structure_api.get_all_with_no_data(
                request.user
            )
        else:
            forms = curate_data_structure_api.get_all_by_user_id_with_no_data(
                request.user.id
            )
        return forms

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
            custom_resource_api.get_all_of_current_template(
                request=request
            ).order_by("sort")
        )
        # Get arguments
        tab = request.GET.get("ispublished", "all")
        tab = (
            tab
            if tab in ["all", "published", "unpublished", "draft", "other"]
            else "all"
        )
        page = request.GET.get("page", 1)
        if tab == "draft":
            document = (
                dashboard_common_constants.FUNCTIONAL_OBJECT_ENUM.FORM.value
            )
            template = (
                dashboard_constants.DASHBOARD_FORMS_TEMPLATE_TABLE_PAGINATION
            )
        else:
            document = (
                dashboard_common_constants.FUNCTIONAL_OBJECT_ENUM.RECORD.value
            )
            template = self.data_template

        context = {
            "page": page,
            "roles": ",".join(request.GET.getlist("role", [cr_type_all.slug])),
            "ispublished": tab,
        }

        # Get resources
        if tab == "draft":
            filtered_data = self.load_drafts(request)
        elif tab == "other":
            filtered_data = self.load_other_records(request)
        else:
            filtered_data = self.load_records(request, tab, custom_resources)

        # Paginator
        results_paginator = ResultsPaginator.get_results(
            filtered_data, page, settings.RECORD_PER_PAGE_PAGINATION
        )

        # Data context
        if tab in ["all", "published", "unpublished", "other"]:
            results_paginator.object_list = self._format_data_context_registry(
                results_paginator.object_list,
            )
        elif tab == "draft":
            results_paginator.object_list = (
                self._format_draft_context_registry(
                    results_paginator.object_list,
                )
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
                "action_form": ActionForm(
                    [("2", "Change owner of selected records")]
                ),
                "menu": self.administration,
                "administration": self.administration,
                "username_list": get_id_username_dict(
                    user_api.get_all_users()
                ),
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
                        if custom_resource_api._is_custom_resource_type_resource(
                            cr
                        )
                        and cr.display_icon
                    ]
                ),
                "type_resource": CUSTOM_RESOURCE_TYPE.RESOURCE.value,
                "ALLOW_MULTIPLE_SCHEMAS": ALLOW_MULTIPLE_SCHEMAS,
            }
        )

        modals = [
            "core_main_app/user/workspaces/list/modals/assign_workspace.html",
            dashboard_common_constants.MODALS_COMMON_DELETE,
            dashboard_common_constants.MODALS_COMMON_CHANGE_OWNER,
            EditDataView.get_modal_html_path(),
        ]

        assets = self._get_assets()

        # Set page title
        context.update({"page_title": "Dashboard"})

        return self.common_render(
            request,
            self.template,
            context=context,
            assets=assets,
            modals=modals,
        )

    def _format_data_context_registry(self, data_list):
        """Format context for registry data

        Args:
            data_list:

        Returns:

        """
        data_context_list = []
        username_list = dict(
            (x.id, x.username) for x in user_api.get_all_users()
        )
        for data in data_list:
            forms_count = (
                len(
                    curate_data_structure_api.get_all_curate_data_structures_by_data(
                        data, self.request.user
                    )
                )
                if self.administration
                else 0
            )
            data_role = get_role(data)
            data_context_list.append(
                {
                    "data": data,
                    "username_list": username_list,
                    "data_status": get_status(data),
                    "data_status_values": DataStatus,
                    "data_role": ", ".join(
                        [
                            _get_role_label(x, request=self.request)
                            for x in data_role
                        ]
                    )
                    if data_role
                    else None,
                    "form_id": _get_form_id(data, self.request.user),
                    "forms_count": forms_count,
                    "can_read": True,
                    "can_write": True,
                    "is_owner": True,
                    "can_change_workspace": check_if_workspace_can_be_changed(
                        data
                    ),
                    "can_set_public": not data_api.is_data_public(data),
                    "delete_url": reverse(
                        "admin:core_main_app_data_delete", args=(data.id,)
                    )
                    if self.administration
                    else None,
                }
            )
        return data_context_list

    def _format_draft_context_registry(self, draft_list):
        """Format context for registry draft

        Args:
            draft_list:

        Returns:

        """
        draft_context_list = []
        for draft in draft_list:
            try:
                role = ", ".join(
                    [
                        custom_resource_api.get_by_role_for_current_template(
                            x, request=self.request
                        ).title
                        for x in curate_data_structure_registry_api.get_role(
                            draft
                        )
                    ]
                    if draft.form_string
                    else ["None"]
                )
            except exceptions.XMLError:
                role = "None"
            except exceptions.ModelError:
                role = "None"
            draft_context_list.append({"form": draft, "role": role})
        return draft_context_list

    def _get_assets(self):
        # add js & css for the super class
        assets = super()._get_assets()
        # add css relatives to the registry
        assets["css"].append(
            "core_dashboard_registry_app/user/css/list/records.css"
        )
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
            {
                "path": "core_dashboard_registry_app/user/js/list/open_form.raw.js",
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
            {
                "path": "core_dashboard_registry_app/user/js/get_url.js",
                "is_raw": False,
            }
        )
        assets["js"].append(EditDataView.get_modal_js_path())
        return assets


class DashboardRegistryWorkspaceRecords(DashboardWorkspaceRecords):
    """List the records of a workspace for the registry."""

    def _format_data_context(
        self, data_list, user, user_can_read, user_can_write
    ):
        detailed_user_data = []
        username_list = get_id_username_dict(user_api.get_all_users())
        for data in data_list:
            forms_count = (
                len(
                    curate_data_structure_api.get_all_curate_data_structures_by_data(
                        data, self.request.user
                    )
                )
                if self.administration
                else 0
            )
            is_owner = str(data.user_id) == str(user.id) or self.administration
            data_role = get_role(data)
            detailed_user_data.append(
                {
                    "data": data,
                    "username_list": username_list,
                    "data_status": get_status(data),
                    "data_status_values": DataStatus,
                    "data_role": ", ".join(
                        [
                            _get_role_label(x, request=self.request)
                            for x in data_role
                        ]
                    )
                    if data_role
                    else None,
                    "form_id": _get_form_id(data, self.request.user),
                    "forms_count": forms_count,
                    "can_read": user_can_read or is_owner,
                    "can_write": user_can_write or is_owner,
                    "is_owner": is_owner,
                    "can_set_public": not data_api.is_data_public(data),
                    "delete_url": reverse(
                        "admin:core_main_app_data_delete", args=(data.id,)
                    )
                    if self.administration
                    else None,
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
        assets["css"].append(
            "core_dashboard_registry_app/user/css/list/records.css"
        )
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
            {
                "path": "core_dashboard_registry_app/user/js/get_url.js",
                "is_raw": False,
            }
        )
        assets["js"].append(
            {"path": dashboard_constants.JS_PUBLISH_RESOURCE, "is_raw": False}
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
                        for x in curate_data_structure_registry_api.get_role(
                            form
                        )
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


def _get_form_id(data, user):
    """Get form id by data and user

    Args:
        data:
        user

    Returns:

    """
    try:
        return curate_data_structure_api.get_by_data_id_and_user(
            data.id, user
        ).id
    except DoesNotExist:
        return None
