"""Tests for DRF Insights Pagination paginator."""

from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from drf_insights_pagination import pagination
from drf_insights_pagination.settings import insights_pagination_settings

factory = APIRequestFactory()


class InsightsPaginationTests(TestCase):
    """InsightsPagination test class."""

    def setUp(self):
        """Set up a bunch of test data."""
        self.app_path = insights_pagination_settings.APP_PATH

        class ExamplePagination(pagination.InsightsPagination):
            default_limit = 10
            max_limit = 15

        self.pagination = ExamplePagination()
        self.queryset = range(1, 101)

    def paginate_queryset(self, request):
        """Paginate the queryset."""
        return list(self.pagination.paginate_queryset(self.queryset, request))

    def get_paginated_content(self, queryset):
        """Get paginated data."""
        response = self.pagination.get_paginated_response(queryset)
        return response.data

    def test_insights_pagination(self):
        """Test insights paginator."""
        path = "/v3/object/"
        request = Request(factory.get(path, {"limit": 5, "offset": 1}))
        queryset = self.paginate_queryset(request)
        content = self.get_paginated_content(queryset)
        assert queryset == [2, 3, 4, 5, 6]
        assert content == {
            "data": [2, 3, 4, 5, 6],
            "links": {
                "first": f"{self.app_path}{path}?limit=5&offset=0",
                "next": f"{self.app_path}{path}?limit=5&offset=6",
                "previous": f"{self.app_path}{path}?limit=5",
                "last": f"{self.app_path}{path}?limit=5&offset=95",
            },
            "meta": {"count": 100},
        }

    def test_insights_pagination_no_next_no_previous_link(self):
        """Test insights paginator with no next or previous link."""
        path = "/v3/object/"
        self.queryset = range(1, 5)
        request = Request(factory.get(path))
        queryset = self.paginate_queryset(request)
        content = self.get_paginated_content(queryset)
        assert queryset == [1, 2, 3, 4]
        assert content == {
            "data": [1, 2, 3, 4],
            "links": {
                "first": f"{self.app_path}{path}?limit=10&offset=0",
                "next": None,
                "previous": None,
                "last": f"{self.app_path}{path}?limit=10&offset=0",
            },
            "meta": {"count": 4},
        }

    def test_insights_pagination_offset(self):
        """Test insights paginator with bigger offset than limit."""
        path = "/v3/object/"
        self.queryset = range(1, 10)
        request = Request(factory.get(path, {"limit": 1, "offset": 5}))
        queryset = self.paginate_queryset(request)
        content = self.get_paginated_content(queryset)
        assert queryset == [6]
        assert content == {
            "data": [6],
            "links": {
                "first": f"{self.app_path}{path}?limit=1&offset=0",
                "next": f"{self.app_path}{path}?limit=1&offset=6",
                "previous": f"{self.app_path}{path}?limit=1&offset=4",
                "last": f"{self.app_path}{path}?limit=1&offset=8",
            },
            "meta": {"count": 9},
        }

    def test_insights_pagination_different_app_path(self):
        """Test insights paginator with a different app_path."""
        self.pagination.app_path = "/api/application"

        path = "/v3/object/"
        request = Request(factory.get(path, {"limit": 5, "offset": 1}))
        queryset = self.paginate_queryset(request)
        content = self.get_paginated_content(queryset)
        assert queryset == [2, 3, 4, 5, 6]
        assert content == {
            "data": [2, 3, 4, 5, 6],
            "links": {
                "first": f"{self.pagination.app_path}{path}?limit=5&offset=0",
                "next": f"{self.pagination.app_path}{path}?limit=5&offset=6",
                "previous": f"{self.pagination.app_path}{path}?limit=5",
                "last": f"{self.pagination.app_path}{path}?limit=5&offset=95",
            },
            "meta": {"count": 100},
        }
