""" User Dashboard menu
"""
from django.urls import reverse
from menu import Menu, MenuItem


from core_dashboard_common_app.constants import FUNCTIONAL_OBJECT_ENUM
from core_dashboard_common_app.templatetags.special_plural import special_case_plural
from core_main_registry_app.settings import ENABLE_BLOB_ENDPOINTS
import core_dashboard_registry_app.settings as settings

Menu.add_item(
    "dashboard",
    MenuItem(
        f"{special_case_plural(FUNCTIONAL_OBJECT_ENUM.RECORD.value.title())}",
        reverse("core_dashboard_records"),
    ),
)
if ENABLE_BLOB_ENDPOINTS:
    Menu.add_item(
        "dashboard",
        MenuItem(
            f"{special_case_plural(FUNCTIONAL_OBJECT_ENUM.FILE.value.title())}",
            reverse("core_dashboard_files"),
        ),
    )
Menu.add_item(
    "dashboard",
    MenuItem(
        f"{special_case_plural(FUNCTIONAL_OBJECT_ENUM.WORKSPACE.value.title())}",
        reverse("core_dashboard_workspaces"),
    ),
)

Menu.add_item(
    "dashboard",
    MenuItem(
        f"{special_case_plural(FUNCTIONAL_OBJECT_ENUM.QUERY.value.title())}",
        reverse("core_dashboard_queries"),
    ),
)

sharing_children = (
    MenuItem(
        f"All {special_case_plural(FUNCTIONAL_OBJECT_ENUM.RECORD.value.title())}",
        reverse("core-admin:core_dashboard_records"),
        icon="list",
    ),
    MenuItem(
        f"All {special_case_plural(FUNCTIONAL_OBJECT_ENUM.WORKSPACE.value.title())}",
        reverse("core-admin:core_dashboard_workspaces"),
        icon="list",
    ),
    MenuItem(
        f"All {special_case_plural(FUNCTIONAL_OBJECT_ENUM.QUERY.value.title())}",
        reverse("core-admin:core_dashboard_queries"),
        icon="list",
    ),
)
if ENABLE_BLOB_ENDPOINTS:
    sharing_children = sharing_children + (
        MenuItem(
            f"All {special_case_plural(FUNCTIONAL_OBJECT_ENUM.FILE.value.title())}",
            reverse("core-admin:core_dashboard_files"),
            icon="list",
        ),
    )

if "core_curate_app" in settings.INSTALLED_APPS:
    Menu.add_item(
        "dashboard",
        MenuItem(
            f"{special_case_plural(FUNCTIONAL_OBJECT_ENUM.FORM.value.title())}",
            reverse("core_dashboard_forms"),
        ),
    )
    sharing_children += (
        MenuItem(
            f"All {special_case_plural(FUNCTIONAL_OBJECT_ENUM.FORM.value.title())}",
            reverse("core-admin:core_dashboard_forms"),
            icon="list",
        ),
    )

Menu.add_item("user", MenuItem("My Profile", reverse("core_dashboard_profile")))

Menu.add_item("admin", MenuItem("DASHBOARD", None, children=sharing_children))

Menu.add_item(
    "main",
    MenuItem(
        "Dashboard",
        reverse("core_dashboard_home"),
        check=lambda request: request.user.is_authenticated,
    ),
)
