"""
Url router for the administration site
"""
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path

from core_dashboard_common_app import constants as dashboard_constants
from core_dashboard_common_app.views.common import views as common_views
from core_explore_common_app.views.user import ajax as user_ajax
from core_main_app.admin import core_admin_site
from core_main_registry_app.settings import ENABLE_BLOB_ENDPOINTS
from core_dashboard_registry_app.views.common import (
    views as registry_common_views,
)
from core_dashboard_registry_app.views.common.ajax import EditDataView


admin_urls = [
    # Admin
    re_path(
        r"^records$",
        staff_member_required(
            registry_common_views.DashboardRegistryRecords.as_view(
                allow_change_workspace_if_public=False,
                administration=True,
                template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
            )
        ),
        name="core_dashboard_records",
    ),
    re_path(
        r"^forms$",
        staff_member_required(
            registry_common_views.DashboardRegistryForms.as_view(
                document=dashboard_constants.FUNCTIONAL_OBJECT_ENUM.FORM.value,
                administration=True,
                template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
            )
        ),
        name="core_dashboard_forms",
    ),
    re_path(
        r"^workspaces$",
        staff_member_required(
            common_views.DashboardWorkspaces.as_view(
                administration=True,
                template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
            )
        ),
        name="core_dashboard_workspaces",
    ),
    re_path(
        r"^queries",
        staff_member_required(
            common_views.DashboardQueries.as_view(
                administration=True,
                template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
            )
        ),
        name="core_dashboard_queries",
    ),
    re_path(
        r"^query/(?P<persistent_query_type>\w+)/(?P<persistent_query_id>\w+)",
        staff_member_required(
            user_ajax.ContentPersistentQueryView.as_view(
                administration=True,
                template="core_explore_common_app/admin/persistent_query/view_query_content.html",
            )
        ),
        name="core_explore_common_persistent_query_content",
    ),
    re_path(
        r"^workspace-list-records/(?P<workspace_id>\w+)$",
        staff_member_required(
            registry_common_views.DashboardRegistryWorkspaceRecords.as_view(
                administration=True,
                template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
            )
        ),
        name="core_dashboard_workspace_list",
    ),
    re_path(
        r"^dashboard-data/(?P<pk>[\w-]+)/edit/$",
        staff_member_required(EditDataView.as_view()),
        name="core_dashboard_app_edit_data",
    ),
]

if ENABLE_BLOB_ENDPOINTS:
    admin_urls.append(
        re_path(
            r"^files$",
            staff_member_required(
                common_views.DashboardFiles.as_view(
                    administration=True,
                    template=dashboard_constants.ADMIN_DASHBOARD_TEMPLATE,
                )
            ),
            name="core_dashboard_files",
        ),
    )

urls = core_admin_site.get_urls()
core_admin_site.get_urls = lambda: admin_urls + urls
