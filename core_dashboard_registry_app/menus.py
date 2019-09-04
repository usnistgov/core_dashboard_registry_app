"""
    User Dashboard menu
"""
from django.core.urlresolvers import reverse
from menu import Menu, MenuItem

import core_dashboard_registry_app.settings as settings
from core_dashboard_common_app.constants import FUNCTIONAL_OBJECT_ENUM

Menu.add_item(
    "dashboard", MenuItem('{0}s'.format(FUNCTIONAL_OBJECT_ENUM.RECORD.value.title()), reverse('core_dashboard_records'))
)

Menu.add_item(
    "dashboard", MenuItem('{0}s'.format(FUNCTIONAL_OBJECT_ENUM.WORKSPACE.value.title()), reverse('core_dashboard_workspaces'))
)

sharing_children = (
    MenuItem('All {0}s'.format(FUNCTIONAL_OBJECT_ENUM.RECORD.value.title()), reverse("admin:core_dashboard_records"),
             icon="list"),
    MenuItem('All {0}s'.format(FUNCTIONAL_OBJECT_ENUM.WORKSPACE.value.title()), reverse("admin:core_dashboard_workspaces"),
             icon="list"),
)

if 'core_curate_app' in settings.INSTALLED_APPS:
    Menu.add_item(
        "dashboard", MenuItem('{0}s'.format(FUNCTIONAL_OBJECT_ENUM.FORM.value.title()), reverse('core_dashboard_forms'))
    )
    sharing_children += (MenuItem('All {0}s'.format(FUNCTIONAL_OBJECT_ENUM.FORM.value.title()),
                                  reverse("admin:core_dashboard_forms"), icon="list"),)

Menu.add_item(
    "user", MenuItem("My Profile", reverse('core_dashboard_profile'))
)

Menu.add_item(
    "admin", MenuItem("DASHBOARD", None, children=sharing_children)
)

Menu.add_item(
    "main", MenuItem("Dashboard", reverse("core_dashboard_home"), check=lambda request: request.user.is_authenticated())
)
