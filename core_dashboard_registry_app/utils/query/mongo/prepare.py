""" Mongo query builder tools
"""
from core_dashboard_registry_app.constants import PATH_ROLE
from django.conf import settings
from core_main_registry_app.components.template import (
    api as registry_template_api,
)
from core_main_app.components.template import api as template_api


def create_query_dashboard_resources(
    request, role_name_list, administration=False
):
    """Create a query for the dashboard.

    Args:
        request:
        role_name_list:
        administration:

    Returns:
    """
    if settings.MONGODB_INDEXING:
        from mongoengine.queryset.visitor import Q

        template_key = "_template_id"
    else:
        from django.db.models import Q

        template_key = "template"
    query = Q()

    # if at least one role
    if len(role_name_list) > 0:
        for role in role_name_list:
            query |= Q(**{f"{PATH_ROLE.replace('.', '__')}__exact": role})

    # user
    if not administration:
        query &= Q(user_id=str(request.user.id))

    # template
    query &= Q(
        **{
            template_key: registry_template_api.get_current_registry_template(
                request
            ).id
        }
    )

    return query


def create_query_other_resources(request, administration=False):
    """Create a query for the dashboard - list resources not curated with registry template

    Args:
        request:
        administration:

    Returns:
    """
    if settings.MONGODB_INDEXING:
        from mongoengine.queryset.visitor import Q

        template_key = "_template_id__in"
    else:
        from django.db.models import Q

        template_key = "template__in"
    query = Q()

    # user
    if not administration:
        query &= Q(user_id=str(request.user.id))

    # template
    all_templates = template_api.get_all(request=request)
    registry_template = registry_template_api.get_current_registry_template(
        request=request
    )
    other_templates = all_templates.exclude(id=registry_template.id)

    query &= Q(**{template_key: other_templates.values_list("id", flat=True)})

    return query
