from django.urls import path
from .views import CreateComplaintView

urlpatterns=[

    path('complaints/',CreateComplaintView.as_view(),name='complaint'),
]