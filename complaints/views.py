from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils.timezone import now
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import Complaint
from rest_framework.exceptions import ValidationError
from .serializers import *
from users.serializers import WorkerSerializer
from users.models import User


#citizen----------------------------------------------------------------------------------------------------------
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
     
#Officer----------------------------------------------------------------------------------------------------------
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
     
class OfficerComplaintDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ComplaintSerializer

    def get_queryset(self):
        return Complaint.objects.filter(
            assignedOfficer=self.request.user
        )    

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




class OfficerDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        complaints = Complaint.objects.filter(
            assignedOfficer=request.user
        )

        data = {
            "total_assigned": complaints.count(),
            "assigned": complaints.filter(status="assigned").count(),
            "in_progress": complaints.filter(status="in_progress").count(),
            "resolved": complaints.filter(status="resolved").count(),
            "emergency": complaints.filter(priority="emergency").count(),
        }

        return Response(data)
    

#Worker---------------------------------------------------------------------------------------------------------

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

class WorkerComplaintDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ComplaintSerializer

    def get_queryset(self):
        return Complaint.objects.filter(
            assignedWorker=self.request.user
        )

class WorkerDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        complaints = Complaint.objects.filter(
            assignedWorker=request.user
        )

        data = {
            "total_assigned": complaints.count(),
            "assigned": complaints.filter(status="assigned").count(),
            "in_progress": complaints.filter(status="in_progress").count(),
            "resolved": complaints.filter(status="resolved").count(),
            "emergency": complaints.filter(priority="emergency").count(),
        }

        return Response(data)
     
class DepartmentWorkers(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkerSerializer

    def get_queryset(self):
        return User.objects.filter(
            role='worker',
            department=self.request.user.department
        )
    
#ADMIN-----------------------------------------------------------------------------------------------------------
class AdminDashboard(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({
            "total_complaints": Complaint.objects.count(),
            "total_citizens": User.objects.filter(role='citizen').count(),
            "total_officers": User.objects.filter(role='officer').count(),
            "total_workers": User.objects.filter(role='worker').count(),
            "resolved": Complaint.objects.filter(status='resolved').count(),
            "pending": Complaint.objects.filter(status='pending').count(),
        })    