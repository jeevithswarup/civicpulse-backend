from django.urls import path
from .views import CreateComplaintView

urlpatterns=[

    path('createcomplaint/',CreateComplaintView.as_view(),name='createcomplaint'),
]