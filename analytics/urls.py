from django.urls import path
from .views import (
    PlatformStatsView,
    DailyTrendView,
    CategoryDistributionView,
    StatusDistributionView,
    ResolutionTrendView,
)

urlpatterns = [
    path('stats/',                 PlatformStatsView.as_view(),        name='analytics-stats'),
    path('daily-trend/',           DailyTrendView.as_view(),            name='analytics-daily-trend'),
    path('category-distribution/', CategoryDistributionView.as_view(),  name='analytics-category'),
    path('status-distribution/',   StatusDistributionView.as_view(),    name='analytics-status'),
    path('resolution-trend/',      ResolutionTrendView.as_view(),       name='analytics-resolution'),
]
