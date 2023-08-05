"""Insights IPP-12 pagination implementation."""
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param

from drf_insights_pagination.settings import insights_pagination_settings


class InsightsPagination(pagination.LimitOffsetPagination):
    """Standard pagination class that follows IPP-12."""

    default_limit = 10
    max_limit = 100
    app_path = insights_pagination_settings.APP_PATH

    def get_first_link(self):
        """Generate link to first page."""
        url = f"{self.app_path}{self.request.get_full_path()}"
        url = replace_query_param(url, self.offset_query_param, 0)

        return replace_query_param(url, self.limit_query_param, self.limit)

    def get_next_link(self):
        """Generate link to next page."""
        if self.offset + self.limit >= self.count:
            return None

        url = f"{self.app_path}{self.request.get_full_path()}"
        url = replace_query_param(url, self.limit_query_param, self.limit)

        offset = self.offset + self.limit
        return replace_query_param(url, self.offset_query_param, offset)

    def get_previous_link(self):
        """Generate link to previous page."""
        if self.offset <= 0:
            return None

        url = f"{self.app_path}{self.request.get_full_path()}"
        url = replace_query_param(url, self.limit_query_param, self.limit)

        offset = self.offset - self.limit
        if offset <= 0:
            return remove_query_param(url, self.offset_query_param)

        return replace_query_param(url, self.offset_query_param, offset)

    def get_last_link(self):
        """Generate link to last page."""
        offset = self.count - self.limit
        offset = offset if offset >= 0 else 0

        url = f"{self.app_path}{self.request.get_full_path()}"
        url = replace_query_param(url, self.offset_query_param, offset)

        return replace_query_param(url, self.limit_query_param, self.limit)

    def get_paginated_response(self, data):
        """Generate paginated response."""
        return Response(
            {
                "meta": {"count": self.count},
                "links": {
                    "first": self.get_first_link(),
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                    "last": self.get_last_link(),
                },
                "data": data,
            }
        )
