from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils.timezone import now
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import Complaint
from rest_framework.exceptions import ValidationError
from .serializers import *



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

class ComplaintDetail(RetrieveAPIView):
     permission_classes=[IsAuthenticated]
     serializer_class=ComplaintSerializer
     
     def  get_queryset(self):
          return Complaint.objects.filter(createdBy=self.request.user)

class ComplaintDelete(DestroyAPIView):
     permission_classes=[IsAuthenticated]
     serializer_class=ComplaintSerializer

     def get_queryset(self):
          return Complaint.objects.filter(createdBy=self.request.user)
     

class AssignedOfficerView(UpdateAPIView):

     permission_classes=[IsAuthenticated]
     serializer_class=AssignOfficerSerializer
     queryset=Complaint.objects.all()

     def perform_update(self, serializer):
         officer=serializer.validated_data['assignedOfficer']
         if officer.role!='officer':
               raise ValidationError("Selected user is not an officer.")
         serializer.save(status='assigned')


class ListOfficierComplaints(ListAPIView,):
     permission_classes=[IsAuthenticated]
     serializer_class=ComplaintSerializer

     def get_queryset(self):
          return Complaint.objects.filter(assignedOfficer=self.request.user)
     

class UpdateComplaintStatus(UpdateAPIView):
     permission_classes=[IsAuthenticated]
     serializer_class=  UpdateComplaintStatusSerializer

     def get_queryset(self):
          return Complaint.objects.filter(assignedOfficer=self.request.user)
     def perform_update(self, serializer):
        complaint = serializer.save()

        if complaint.status == "resolved":
            complaint.resolved_at = now()
            complaint.save()


class CitizenDashboard(APIView):
     permission_classes=[IsAuthenticated]

     def get(self,request):
          complaints=Complaint.objects.filter(createdBy=request.user)


          data = {
            "my_complaints": complaints.count(),
            "resolved": complaints.filter(status="resolved").count(),
            "pending": complaints.filter(status="pending").count(),
         }

          return Response(data)

class  OfficierDashBoard(APIView):
      permission_classes=[IsAuthenticated]

      def get(self,request):
           complaint=Complaint.objects.filter(assignedOfficer=self.request.user)


#############################  Workers ##############################################################

class AssignedWorkerView(UpdateAPIView):
     permission_classes=[IsAuthenticated]
     serializer_class=AssignedWorkerSerialializer
     queryset=Complaint.objects.all()


     def perform_update(self, serializer):
          worker=serializer.validated_data['assignedWorker']

          if worker.role!='worker':
                   raise ValidationError("Selected user is not an worker.")
          if worker.department != self.request.user.department:
            raise ValidationError("Worker must belong to your department.")
          
          serializer.save(status='in_progress')

class AssignedWorkerComplaints(ListAPIView):
     permission_classes=[IsAuthenticated]
     serializer_class=ComplaintSerializer

     def get_queryset(self):
          return Complaint.objects.filter(assignedWorker=self.request.user)

class WorkerUpdateComplaint(UpdateAPIView):
     permission_classes=[IsAuthenticated]
     serializer_class=WorkerUpdateSerializer

     def get_queryset(self):
          return Complaint.objects.filter(assignedWorker=self.request.user)
     def perform_update(self, serializer):
          complaint=serializer.save()

          if complaint.status=='resolved':
                complaint.resolved_at = now()
                complaint.save()






