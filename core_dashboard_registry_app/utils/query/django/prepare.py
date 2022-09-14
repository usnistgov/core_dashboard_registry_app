""" Mongo query builder tools
"""
from django.db.models import Q

from core_dashboard_registry_app.constants import PATH_ROLE


def create_query_dashboard_resources(request, role_name_list, administration):
    """Create a query for the dashboard.

    Args:
        request:
        role_name_list:
        administration:

    Returns:
    """
    query = Q()

    # if at least one role
    if len(role_name_list) > 0:
        for role in role_name_list:
            query |= Q(**{PATH_ROLE.replace(".", "__"): role})

    # user
    if not administration:
        query &= Q(user_id=request.user.id)

    return query
