from django.urls import path
from .views import *

urlpatterns=[

    path('createcomplaint/',CreateComplaintView.as_view(),name='createcomplaint'),
    path('my/',MyComplaints.as_view(),name='mycomplaints'),
    path('updatecomplaint/<int:pk>/',UpdateComplaint.as_view(),name='updatecomplaint'),
    path('deletecomplaint/<int:pk>/',ComplaintDelete.as_view(),name='deletecomplaint'),  
    path('assign-officer/<int:pk>/',AssignedOfficerView.as_view(),name='assign-officer'), 
    path('officers-complaints/',ListOfficierComplaints.as_view(),name='officers-complaints'),
    path('status-update/',UpdateComplaintStatus.as_view(),name='status-update'),
    path('citizen-dashboard',CitizenDashboard.as_view,name='citizen-dashboard'),
    path('assign-worker/<int:pk>/',AssignedWorkerView.as_view(),name='assign-worker'),
    path('worker-complaints',AssignedWorkerComplaints.as_view,name='worker-complaints'),
    
]