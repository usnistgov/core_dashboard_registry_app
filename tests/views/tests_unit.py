""" Unit tests views
"""
from unittest.mock import patch, MagicMock

from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.test import RequestFactory, override_settings, tag

from core_dashboard_registry_app.views.common.views import (
    DashboardRegistryRecords,
)
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestDashboardRegistryRecords(MongoIntegrationBaseTestCase):
    """TestViewData"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()

    def test_anonymous_user_permission_denied(self):
        """test_anonymous_user_permission_denied

        Returns:

        """
        request = self.factory.get("core_dashboard_records")
        request.user = self.anonymous
        response = DashboardRegistryRecords.as_view()(request)
        self.assertEqual(response.status_code, 302)

    @patch("core_main_app.views.common.views.CommonView.common_render")
    @patch("core_main_app.components.data.api.execute_query")
    @patch(
        "core_main_registry_app.components.custom_resource.api.get_current_custom_resource_type_all"
    )
    @patch(
        "core_main_registry_app.components.custom_resource.api.get_all_of_current_template"
    )
    def test_a_user_can_access_using_psql(
        self,
        get_all_of_current_template,
        get_current_custom_resource_type_all,
        execute_query,
        common_render,
    ):
        """test_a_user_can_access_using_psql

        Returns:

        """
        # Arrange
        cr_type_all = MagicMock()
        cr_type_all.slug = "test"

        current_template = MagicMock()
        execute_query.return_value = []

        expected_response = HttpResponse()
        common_render.return_value = expected_response

        get_current_custom_resource_type_all.return_value = cr_type_all
        get_all_of_current_template.return_value = current_template
        request = self.factory.get("core_dashboard_records")
        request.user = self.user1

        # Act
        response = DashboardRegistryRecords.as_view()(request)

        # Assert
        self.assertEqual(response, expected_response)

    @patch("core_main_app.views.common.views.CommonView.common_render")
    @patch("core_main_app.components.mongo.api.execute_mongo_query")
    @patch(
        "core_main_registry_app.components.custom_resource.api.get_current_custom_resource_type_all"
    )
    @patch(
        "core_main_registry_app.components.custom_resource.api.get_all_of_current_template"
    )
    @override_settings(MONGODB_INDEXING=True)
    @tag("mongodb")
    def test_a_user_can_access_using_mongodb(
        self,
        get_all_of_current_template,
        get_current_custom_resource_type_all,
        execute_query,
        common_render,
    ):
        """test_a_user_can_access_using_mongodb

        Returns:

        """
        # Arrange
        cr_type_all = MagicMock()
        cr_type_all.slug = "test"

        current_template = MagicMock()
        execute_query.return_value = []

        expected_response = HttpResponse()
        common_render.return_value = expected_response

        get_current_custom_resource_type_all.return_value = cr_type_all
        get_all_of_current_template.return_value = current_template
        request = self.factory.get("core_dashboard_records")
        request.user = self.user1

        # Act
        response = DashboardRegistryRecords.as_view()(request)

        # Assert
        self.assertEqual(response, expected_response)
