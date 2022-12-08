""" Mongo query builder tools
"""
from core_dashboard_registry_app.constants import PATH_ROLE
from django.conf import settings


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
    else:
        from django.db.models import Q
    query = Q()

    # if at least one role
    if len(role_name_list) > 0:
        for role in role_name_list:
            query |= Q(**{f"{PATH_ROLE.replace('.', '__')}__exact": role})

    # user
    if not administration:
        query &= Q(user_id=str(request.user.id))

    return query
