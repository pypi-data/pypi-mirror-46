# DRF Insights Pagination

A simple library to add a paginator to DRF that follows Insights IPP-12.

### Installation and Usage

Install the library

```
pip install drf-insights-pagination
```

Change your pagination class, and optionally `APP_PATH` in your settings

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'drf_insights_pagination.pagination.InsightsPagination',
}
INSIGHTS_PAGINATION_APP_PATH = '/api/application'
```

