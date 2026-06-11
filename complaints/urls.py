from django.urls import path
from .views import *

urlpatterns=[

    path('createcomplaint/',CreateComplaintView.as_view(),name='createcomplaint'),
    path('my/',MyComplaints.as_view(),name='mycomplaints'),
    path('updatecomplaint/<int:pk>/',UpdateComplaint,name='updatecomplaint'),
]