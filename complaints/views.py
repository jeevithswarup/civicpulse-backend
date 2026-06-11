from django.shortcuts import render
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from .models import Complaint
from .serializers import ComplaintSerializer



class CreateComplaintView(CreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Complaint.objects.all()
    serializer_class=ComplaintSerializer

    def perform_create(self, serializer):
        serializer.save(createdBy=self.request.user)

class MyComplaints(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=ComplaintSerializer

    def get_queryset(self):
          return Complaint.objects.filter(createdBy=self.request.user)

class UpdateComplaint(UpdateAPIView):
     permission_classes=[IsAuthenticated]
     serializer_class=ComplaintSerializer

     def get_queryset(self):
          return Complaint.objects.filter(createdBy=self.request.user)