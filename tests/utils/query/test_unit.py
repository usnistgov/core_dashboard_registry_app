"""Query tool unit tests
"""
from unittest import TestCase

from django.test import override_settings, tag

from core_dashboard_registry_app.utils.query.mongo.prepare import (
    create_query_dashboard_resources,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request


class TestCreateDashboardResource(TestCase):
    """TestCompileRegex"""

    def test_create_query_dashboard_resources_psql(self):
        """test_create_query_dashboard_resources_psql

        Returns:

        """
        from django.db.models import Q

        # Arrange
        mock_user = create_mock_user("1")
        mock_request = create_mock_request(user=mock_user)
        expected_query = Q(
            **{
                "dict_content__Resource__role__@xsi:type__exact": "Organization"
            }
        ) & Q(**{"user_id": "1"})
        # Act
        query = create_query_dashboard_resources(
            mock_request, ["Organization"]
        )

        # Assert
        self.assertTrue(isinstance(query, Q))
        self.assertEqual(query, expected_query)

    def test_create_query_dashboard_resources_for_admin_psql(self):
        """test_create_query_dashboard_resources_for_admin_psql

        Returns:

        """
        from django.db.models import Q

        # Arrange
        mock_user = create_mock_user("1")
        mock_request = create_mock_request(user=mock_user)
        expected_query = Q(
            **{
                "dict_content__Resource__role__@xsi:type__exact": "Organization"
            }
        )
        # Act
        query = create_query_dashboard_resources(
            mock_request, ["Organization"], administration=True
        )

        # Assert
        self.assertTrue(isinstance(query, Q))
        self.assertEqual(query, expected_query)

    @override_settings(MONGODB_INDEXING=True)
    @tag("mongodb")
    def test_create_query_dashboard_resources_mongodb(self):
        """test_create_query_dashboard_resources_mongodb

        Returns:

        """
        from mongoengine.queryset.visitor import QCombination, Q

        # Arrange
        mock_user = create_mock_user("1")
        mock_request = create_mock_request(user=mock_user)
        expected_query = Q(
            **{
                "dict_content__Resource__role__@xsi:type__exact": "Organization"
            }
        ) & Q(**{"user_id": "1"})
        # Act
        query = create_query_dashboard_resources(
            mock_request, ["Organization"]
        )

        # Assert
        self.assertTrue(isinstance(query, QCombination))
        self.assertEqual(query, expected_query)

    @override_settings(MONGODB_INDEXING=True)
    @tag("mongodb")
    def test_create_query_dashboard_resources_for_admin_mongodb(self):
        """test_create_query_dashboard_resources_for_admin_mongodb

        Returns:

        """
        from mongoengine.queryset.visitor import Q

        # Arrange
        mock_user = create_mock_user("1")
        mock_request = create_mock_request(user=mock_user)
        expected_query = Q(
            **{
                "dict_content__Resource__role__@xsi:type__exact": "Organization"
            }
        )
        # Act
        query = create_query_dashboard_resources(
            mock_request, ["Organization"], administration=True
        )

        # Assert
        self.assertTrue(isinstance(query, Q))
        self.assertEqual(query, expected_query)
