""" Mongo query builder tools
"""
from core_dashboard_registry_app.constants import PATH_ROLE


def create_query_dashboard_resources(request, role_name_list, administration):
    """Create a query for the dashboard.

    Args:
        request:
        role_name_list:
        administration:

    Returns:
    """
    query = {}

    # if at least one role
    if len(role_name_list) > 0:
        query["$or"] = [{PATH_ROLE: role} for role in role_name_list]

    # user
    if not administration:
        query["user_id"] = str(request.user.id)

    return query
