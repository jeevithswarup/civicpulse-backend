from django.urls import path
from .views import *

urlpatterns=[

    #citizen---------------------------------------------------------------------------------------
    path('citizen-dashboard/',CitizenDashboard.as_view,name='citizen-dashboard'),
    path('createcomplaint/',CreateComplaintView.as_view(),name='createcomplaint'),
    path('my/',MyComplaints.as_view(),name='mycomplaints'),
    path('updatecomplaint/<int:pk>/',UpdateComplaint.as_view(),name='updatecomplaint'),
    path('deletecomplaint/<int:pk>/',ComplaintDelete.as_view(),name='deletecomplaint'),  


    #officer----------------------------------------------------------------------------------------
    path('officer/dashboard/', OfficerDashboard.as_view()),
    path('assign-officer/<int:pk>/',AssignedOfficerView.as_view(),name='assign-officer'), 
    path('officers-complaints/',ListOfficierComplaints.as_view(),name='officers-complaints'),
    path('status-update/',UpdateComplaintStatus.as_view(),name='status-update'),
    path('officer/workers/',DepartmentWorkers.as_view(),name='officer-workers'),

    
    #Workers----------------------------------------------------------------------------------------
    path('worker-dashboard/',WorkerDashboard.as_view(),name='worker-dashboard'),
    path('assign-worker/<int:pk>/',AssignedWorkerView.as_view(),name='assign-worker'),
    path('worker-complaints/',AssignedWorkerComplaints.as_view(),name='worker-complaints'),
    path('complaint-update/<int:pk>/',WorkerUpdateComplaint.as_view(),name='complaint-update'),
    path('worker/complaints/<int:pk>/', WorkerComplaintDetail.as_view(),name='worker-complaint'),
  


    #Admin-------------------------------------------------------------------------------------------
    path('admin-dashboard/',AdminDashboard.as_view(),name='admin-dashboard'),

#-------------------------------------------------------------------------------------------------------
    path('complaints/<int:pk>/support/',SupportComplaintView.as_view(),name='support-complaint'),
   
]