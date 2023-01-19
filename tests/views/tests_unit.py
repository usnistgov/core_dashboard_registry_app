""" Unit tests views
"""
from unittest.mock import patch, MagicMock

from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.test import RequestFactory, override_settings, tag

from core_dashboard_registry_app.views.common.views import (
    DashboardRegistryRecords,
)
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import ModelError
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
    @patch("core_main_app.components.data.api.execute_query")
    @patch(
        "core_main_registry_app.components.custom_resource.api.get_current_custom_resource_type_all"
    )
    @patch(
        "core_main_registry_app.components.custom_resource.api.get_all_of_current_template"
    )
    def test_user_without_required_perm_get_no_results(
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
        execute_query.side_effect = AccessControlError("Error")
        expected_response = HttpResponse()
        common_render.return_value = expected_response

        get_current_custom_resource_type_all.return_value = cr_type_all
        get_all_of_current_template.return_value = current_template
        request = self.factory.get("core_dashboard_records")
        request.user = self.user1

        # Act
        response = DashboardRegistryRecords.as_view()(request)
        self.assertEqual(response.status_code, 200)

    @patch("core_main_app.components.workspace.api.get_global_workspace")
    @patch("core_main_app.views.common.views.CommonView.common_render")
    @patch("core_main_app.components.data.api.execute_query")
    @patch(
        "core_main_registry_app.components.custom_resource.api.get_current_custom_resource_type_all"
    )
    @patch(
        "core_main_registry_app.components.custom_resource.api.get_all_of_current_template"
    )
    def test_request_published_records(
        self,
        get_all_of_current_template,
        get_current_custom_resource_type_all,
        execute_query,
        common_render,
        get_global_workspace,
    ):
        """test_request_published_records

        Returns:

        """
        # Arrange
        cr_type_all = MagicMock()
        cr_type_all.slug = "test"

        current_template = MagicMock()
        loaded_data = MagicMock()
        loaded_data.filter.return_value = []
        execute_query.return_value = loaded_data

        expected_response = HttpResponse()
        common_render.return_value = expected_response

        workspace = MagicMock()
        workspace.id = 1
        get_global_workspace.return_value = workspace

        get_current_custom_resource_type_all.return_value = cr_type_all
        get_all_of_current_template.return_value = current_template
        request = self.factory.get(
            "core_dashboard_records", data={"ispublished": "published"}
        )
        request.user = self.user1

        # Act
        response = DashboardRegistryRecords.as_view()(request)
        self.assertEqual(response.status_code, 200)

    @patch("core_main_app.views.common.views.CommonView.common_render")
    @patch("core_main_app.components.data.api.execute_query")
    @patch(
        "core_main_registry_app.components.custom_resource.api.get_current_custom_resource_type_all"
    )
    @patch(
        "core_main_registry_app.components.custom_resource.api.get_all_of_current_template"
    )
    def test_request_unpublished_records(
        self,
        get_all_of_current_template,
        get_current_custom_resource_type_all,
        execute_query,
        common_render,
    ):
        """test_request_unpublished_records

        Returns:

        """
        # Arrange
        cr_type_all = MagicMock()
        cr_type_all.slug = "test"

        current_template = MagicMock()
        loaded_data = MagicMock()
        loaded_data.filter.return_value = []
        execute_query.return_value = loaded_data

        expected_response = HttpResponse()
        common_render.return_value = expected_response

        get_current_custom_resource_type_all.return_value = cr_type_all
        get_all_of_current_template.return_value = current_template
        request = self.factory.get(
            "core_dashboard_records", data={"ispublished": "unpublished"}
        )
        request.user = self.user1

        # Act
        response = DashboardRegistryRecords.as_view()(request)
        self.assertEqual(response.status_code, 200)

    @patch("core_main_app.views.common.views.CommonView.common_render")
    @patch("core_main_app.components.data.api.execute_query")
    @patch(
        "core_main_registry_app.components.custom_resource.api.get_current_custom_resource_type_all"
    )
    @patch(
        "core_main_registry_app.components.custom_resource.api.get_all_of_current_template"
    )
    def test_request_all_records(
        self,
        get_all_of_current_template,
        get_current_custom_resource_type_all,
        execute_query,
        common_render,
    ):
        """test_request_all_records

        Returns:

        """
        # Arrange
        cr_type_all = MagicMock()
        cr_type_all.slug = "test"

        current_template = MagicMock()
        loaded_data = MagicMock()
        loaded_data.filter.return_value = []
        execute_query.return_value = loaded_data

        expected_response = HttpResponse()
        common_render.return_value = expected_response

        get_current_custom_resource_type_all.return_value = cr_type_all
        get_all_of_current_template.return_value = current_template
        request = self.factory.get(
            "core_dashboard_records", data={"ispublished": "all"}
        )
        request.user = self.user1

        # Act
        response = DashboardRegistryRecords.as_view()(request)
        self.assertEqual(response.status_code, 200)

    @patch("core_main_app.views.common.views.CommonView.common_render")
    @patch("core_main_app.components.data.api.execute_query")
    @patch(
        "core_main_registry_app.components.custom_resource.api.get_current_custom_resource_type_all"
    )
    @patch(
        "core_main_registry_app.components.custom_resource.api.get_all_of_current_template"
    )
    def test_request_drafts(
        self,
        get_all_of_current_template,
        get_current_custom_resource_type_all,
        execute_query,
        common_render,
    ):
        """test_request_drafts

        Returns:

        """
        # Arrange
        cr_type_all = MagicMock()
        cr_type_all.slug = "test"

        current_template = MagicMock()
        loaded_data = MagicMock()
        loaded_data.filter.return_value = []
        execute_query.return_value = loaded_data

        expected_response = HttpResponse()
        common_render.return_value = expected_response

        get_current_custom_resource_type_all.return_value = cr_type_all
        get_all_of_current_template.return_value = current_template
        request = self.factory.get(
            "core_dashboard_records", data={"ispublished": "draft"}
        )
        request.user = self.user1

        # Act
        response = DashboardRegistryRecords.as_view()(request)
        self.assertEqual(response.status_code, 200)

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

    @patch(
        "core_main_registry_app.components.custom_resource.api.get_by_role_for_current_template"
    )
    @patch(
        "core_curate_registry_app.components.curate_data_structure.api.get_role"
    )
    def test_format_draft_context_registry_with_role(
        self,
        get_role,
        get_by_role_for_current_template,
    ):
        """test_format_draft_context_registry_with_role

        Returns:

        """
        # Arrange
        custom_resource = MagicMock()
        custom_resource.title = "test"
        get_by_role_for_current_template.return_value = custom_resource

        get_role.return_value = ["test"]

        draft = MagicMock()
        draft.form_string = "form_string"

        request = self.factory.get("core_dashboard_records")
        request.user = self.user1
        view = DashboardRegistryRecords()
        view.request = request

        # Act
        result = view._format_draft_context_registry(draft_list=[draft])

        # Assert
        self.assertEqual(result[0]["role"], "test")

    @patch(
        "core_main_registry_app.components.custom_resource.api.get_by_role_for_current_template"
    )
    @patch(
        "core_curate_registry_app.components.curate_data_structure.api.get_role"
    )
    def test_format_draft_context_registry_without_role(
        self,
        get_role,
        get_by_role_for_current_template,
    ):
        """test_format_draft_context_registry_without_role

        Returns:

        """
        # Arrange
        custom_resource = MagicMock()
        custom_resource.title = "test"
        get_by_role_for_current_template.return_value = custom_resource

        get_role.return_value = ["test"]

        draft = MagicMock()
        draft.form_string = None

        request = self.factory.get("core_dashboard_records")
        request.user = self.user1
        view = DashboardRegistryRecords()
        view.request = request

        # Act
        result = view._format_draft_context_registry(draft_list=[draft])

        # Assert
        self.assertEqual(result[0]["role"], "None")

    @patch(
        "core_main_registry_app.components.custom_resource.api.get_by_role_for_current_template"
    )
    @patch(
        "core_curate_registry_app.components.curate_data_structure.api.get_role"
    )
    def test_format_draft_context_registry_with_error(
        self,
        get_role,
        get_by_role_for_current_template,
    ):
        """test_format_draft_context_registry_without_role

        Returns:

        """
        # Arrange
        get_by_role_for_current_template.side_effect = ModelError("Error")

        get_role.return_value = ["test"]

        draft = MagicMock()
        draft.form_string = "form_string"

        request = self.factory.get("core_dashboard_records")
        request.user = self.user1
        view = DashboardRegistryRecords()
        view.request = request

        # Act
        result = view._format_draft_context_registry(draft_list=[draft])

        # Assert
        self.assertEqual(result[0]["role"], "None")
