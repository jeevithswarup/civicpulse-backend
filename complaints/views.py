from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Complaint
from .serializers import ComplaintSerializer



class CreateComplaintView(CreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Complaint.objects.all()
    serializer_class=ComplaintSerializer

    def perform_create(self, serializer):
        serializer.save(createdBy=self.request.user)


