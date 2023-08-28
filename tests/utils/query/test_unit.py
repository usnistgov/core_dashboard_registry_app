"""Query tool unit tests
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from django.test import override_settings, tag

from core_dashboard_registry_app.utils.query.mongo.prepare import (
    create_query_dashboard_resources,
    create_query_other_resources,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request


class TestCreateQueryDashboardResource(TestCase):
    """TestCreateQueryDashboardResource"""

    @patch(
        "core_main_registry_app.components.template.api.get_current_registry_template"
    )
    def test_create_query_dashboard_resources_psql(
        self, mock_get_current_registry_template
    ):
        """test_create_query_dashboard_resources_psql

        Returns:

        """
        from django.db.models import Q

        # Arrange
        mock_get_current_registry_template.return_value = MagicMock(id=1)
        mock_user = create_mock_user("1")
        mock_request = create_mock_request(user=mock_user)
        expected_query = (
            Q(
                **{
                    "dict_content__Resource__role__@xsi:type__exact": "Organization"
                }
            )
            & Q(**{"user_id": "1"})
            & Q(**{"template": 1})
        )
        # Act
        query = create_query_dashboard_resources(
            mock_request, ["Organization"]
        )

        # Assert
        self.assertTrue(isinstance(query, Q))
        self.assertEqual(query, expected_query)

    @patch(
        "core_main_registry_app.components.template.api.get_current_registry_template"
    )
    def test_create_query_dashboard_resources_for_admin_psql(
        self, mock_get_current_registry_template
    ):
        """test_create_query_dashboard_resources_for_admin_psql

        Returns:

        """
        from django.db.models import Q

        # Arrange
        mock_get_current_registry_template.return_value = MagicMock(id=1)
        mock_user = create_mock_user("1")
        mock_request = create_mock_request(user=mock_user)
        expected_query = Q(
            **{
                "dict_content__Resource__role__@xsi:type__exact": "Organization"
            }
        ) & Q(**{"template": 1})
        # Act
        query = create_query_dashboard_resources(
            mock_request, ["Organization"], administration=True
        )

        # Assert
        self.assertTrue(isinstance(query, Q))
        self.assertEqual(query, expected_query)

    @override_settings(MONGODB_INDEXING=True)
    @tag("mongodb")
    @patch(
        "core_main_registry_app.components.template.api.get_current_registry_template"
    )
    def test_create_query_dashboard_resources_mongodb(
        self, mock_get_current_registry_template
    ):
        """test_create_query_dashboard_resources_mongodb

        Returns:

        """
        from mongoengine.queryset.visitor import QCombination, Q

        # Arrange
        mock_get_current_registry_template.return_value = MagicMock(id=1)
        mock_user = create_mock_user("1")
        mock_request = create_mock_request(user=mock_user)
        expected_query = (
            Q(
                **{
                    "dict_content__Resource__role__@xsi:type__exact": "Organization"
                }
            )
            & Q(**{"user_id": "1"})
            & Q(**{"_template_id": 1})
        )
        # Act
        query = create_query_dashboard_resources(
            mock_request, ["Organization"]
        )

        # Assert
        self.assertTrue(isinstance(query, QCombination))
        self.assertEqual(query, expected_query)

    @override_settings(MONGODB_INDEXING=True)
    @tag("mongodb")
    @patch(
        "core_main_registry_app.components.template.api.get_current_registry_template"
    )
    def test_create_query_dashboard_resources_for_admin_mongodb(
        self, mock_get_current_registry_template
    ):
        """test_create_query_dashboard_resources_for_admin_mongodb

        Returns:

        """
        from mongoengine.queryset.visitor import QCombination, Q

        # Arrange
        mock_get_current_registry_template.return_value = MagicMock(id=1)
        mock_user = create_mock_user("1")
        mock_request = create_mock_request(user=mock_user)
        expected_query = Q(
            **{
                "dict_content__Resource__role__@xsi:type__exact": "Organization"
            }
        ) & Q(**{"_template_id": 1})
        # Act
        query = create_query_dashboard_resources(
            mock_request, ["Organization"], administration=True
        )

        # Assert
        self.assertTrue(isinstance(query, QCombination))
        self.assertEqual(query, expected_query)


class TestCreateQueryOtherResource(TestCase):
    """TestCreateQueryOtherResource"""

    @patch("core_main_app.components.template.api.get_all")
    @patch(
        "core_main_registry_app.components.template.api.get_current_registry_template"
    )
    def test_create_query_other_resources_psql(
        self, mock_get_current_registry_template, mock_templates_get_all
    ):
        """test_create_query_other_resources_psql

        Returns:

        """
        from django.db.models import Q

        # Arrange
        mock_other_templates = MagicMock()
        mock_other_templates.values_list.return_value = []
        mock_all_templates = MagicMock()
        mock_all_templates.exclude.return_value = mock_other_templates
        mock_templates_get_all.return_value = mock_all_templates
        mock_get_current_registry_template.return_value = MagicMock(id=1)
        mock_user = create_mock_user("1")
        mock_request = create_mock_request(user=mock_user)
        expected_query = Q(**{"user_id": "1"}) & Q(**{"template__in": []})
        # Act
        query = create_query_other_resources(
            mock_request,
        )

        # Assert
        self.assertTrue(isinstance(query, Q))
        self.assertEqual(query, expected_query)

    @patch("core_main_app.components.template.api.get_all")
    @patch(
        "core_main_registry_app.components.template.api.get_current_registry_template"
    )
    def test_create_query_other_resources_for_admin_psql(
        self, mock_get_current_registry_template, mock_templates_get_all
    ):
        """test_create_query_other_resources_for_admin_psql

        Returns:

        """
        from django.db.models import Q

        # Arrange
        mock_other_templates = MagicMock()
        mock_other_templates.values_list.return_value = []
        mock_all_templates = MagicMock()
        mock_all_templates.exclude.return_value = mock_other_templates
        mock_templates_get_all.return_value = mock_all_templates
        mock_get_current_registry_template.return_value = MagicMock(id=1)
        mock_user = create_mock_user("1")
        mock_request = create_mock_request(user=mock_user)
        expected_query = Q(**{"template__in": []})
        # Act
        query = create_query_other_resources(mock_request, administration=True)

        # Assert
        self.assertTrue(isinstance(query, Q))
        self.assertEqual(query, expected_query)

    @override_settings(MONGODB_INDEXING=True)
    @tag("mongodb")
    @patch("core_main_app.components.template.api.get_all")
    @patch(
        "core_main_registry_app.components.template.api.get_current_registry_template"
    )
    def test_create_query_other_resources_mongodb(
        self, mock_get_current_registry_template, mock_templates_get_all
    ):
        """test_create_query_other_resources_mongodb

        Returns:

        """
        from mongoengine.queryset.visitor import QCombination, Q

        # Arrange
        mock_other_templates = MagicMock()
        mock_other_templates.values_list.return_value = []
        mock_all_templates = MagicMock()
        mock_all_templates.exclude.return_value = mock_other_templates
        mock_templates_get_all.return_value = mock_all_templates
        mock_get_current_registry_template.return_value = MagicMock(id=1)
        mock_user = create_mock_user("1")
        mock_request = create_mock_request(user=mock_user)
        expected_query = Q(**{"user_id": "1"}) & Q(**{"_template_id__in": []})
        # Act
        query = create_query_other_resources(
            mock_request,
        )

        # Assert
        self.assertTrue(isinstance(query, QCombination))
        self.assertEqual(query, expected_query)

    @override_settings(MONGODB_INDEXING=True)
    @tag("mongodb")
    @patch("core_main_app.components.template.api.get_all")
    @patch(
        "core_main_registry_app.components.template.api.get_current_registry_template"
    )
    def test_create_query_other_resources_for_admin_mongodb(
        self, mock_get_current_registry_template, mock_templates_get_all
    ):
        """test_create_query_other_resources_for_admin_mongodb

        Returns:

        """
        from mongoengine.queryset.visitor import Q

        # Arrange
        mock_other_templates = MagicMock()
        mock_other_templates.values_list.return_value = []
        mock_all_templates = MagicMock()
        mock_all_templates.exclude.return_value = mock_other_templates
        mock_templates_get_all.return_value = mock_all_templates
        mock_get_current_registry_template.return_value = MagicMock(id=1)
        mock_user = create_mock_user("1")
        mock_request = create_mock_request(user=mock_user)
        expected_query = Q(**{"_template_id__in": []})
        # Act
        query = create_query_other_resources(mock_request, administration=True)

        # Assert
        self.assertTrue(isinstance(query, Q))
        self.assertEqual(query, expected_query)
