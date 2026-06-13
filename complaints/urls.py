from django.urls import path
from .views import *

urlpatterns=[

    path('createcomplaint/',CreateComplaintView.as_view(),name='createcomplaint'),
    path('my/',MyComplaints.as_view(),name='mycomplaints'),
    path('updatecomplaint/<int:pk>/',UpdateComplaint,name='updatecomplaint'),
    path('deletecomplaint/<int:pk>/',ComplaintDelete,name='deletecomplaint'),  
    path('assign-officer<int:pk>/',AssignedOfficerView,name='assign-officer'), 
    path('officers-complaints/',ListOfficierComplaints,name='officers-complaints'),
    
]