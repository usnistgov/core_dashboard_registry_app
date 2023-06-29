"""
    Url router for the user dashboard
"""
from django.contrib.auth.decorators import login_required
from django.urls import re_path

from core_dashboard_common_app import constants as dashboard_constants
from core_dashboard_common_app.views.common import ajax, views as common_views
from core_dashboard_registry_app.views.common import (
    ajax as registry_common_ajax,
)
from core_dashboard_registry_app.views.common import (
    views as registry_common_views,
)
from core_dashboard_registry_app.views.common.ajax import EditDataView
from core_main_registry_app.settings import ENABLE_BLOB_ENDPOINTS

urlpatterns = [
    # Common
    re_path(r"^$", registry_common_views.home, name="core_dashboard_home"),
    re_path(
        r"^my-profile$", common_views.my_profile, name="core_dashboard_profile"
    ),
    re_path(
        r"^my-profile/edit$",
        common_views.my_profile_edit,
        name="core_dashboard_profile_edit",
    ),
    re_path(
        r"^delete-document",
        ajax.delete_document,
        name="core_dashboard_delete_document",
    ),
    re_path(
        r"^change-owner",
        ajax.change_owner_document,
        name="core_dashboard_change_owner_document",
    ),
    re_path(
        r"^edit-record", ajax.edit_record, name="core_dashboard_edit_record"
    ),
    # User
    re_path(
        r"^records$",
        login_required(
            registry_common_views.DashboardRegistryRecords.as_view(
                document=dashboard_constants.FUNCTIONAL_OBJECT_ENUM.RECORD.value,
                data_template="core_dashboard_registry_app/list/my_dashboard_my_records_table_pagination.html",
                allow_change_workspace_if_public=False,
            ),
        ),
        name="core_dashboard_records",
    ),
    re_path(
        r"^switch-status-record",
        registry_common_ajax.switch_data_status,
        name="core_dashboard_switch_status_record",
    ),
    re_path(
        r"^forms$",
        login_required(
            registry_common_views.DashboardRegistryForms.as_view(
                document=dashboard_constants.FUNCTIONAL_OBJECT_ENUM.FORM.value
            ),
        ),
        name="core_dashboard_forms",
    ),
    re_path(
        r"^workspaces$",
        login_required(
            common_views.DashboardWorkspaces.as_view(),
        ),
        name="core_dashboard_workspaces",
    ),
    re_path(
        r"^queries",
        login_required(
            common_views.DashboardQueries.as_view(),
        ),
        name="core_dashboard_queries",
    ),
    re_path(
        r"^workspace-list-records/(?P<workspace_id>\w+)$",
        login_required(
            registry_common_views.DashboardRegistryWorkspaceRecords.as_view(
                data_template="core_dashboard_registry_app/list/my_dashboard_my_records_table_pagination.html"
            ),
        ),
        name="core_dashboard_workspace_list",
    ),
    re_path(
        r"^publish-resource",
        registry_common_ajax.publish,
        name="core_dashboard_publish_resource_registry",
    ),
    re_path(
        r"^dashboard-data/(?P<pk>[\w-]+)/edit/$",
        EditDataView.as_view(),
        name="core_dashboard_app_edit_data",
    ),
]

if ENABLE_BLOB_ENDPOINTS:
    urlpatterns.append(
        re_path(
            r"^files$",
            login_required(
                common_views.DashboardFiles.as_view(),
            ),
            name="core_dashboard_files",
        ),
    )
