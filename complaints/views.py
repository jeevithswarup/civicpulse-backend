from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils.timezone import now
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.exceptions import ValidationError
from .serializers import *
from users.serializers import WorkerSerializer
from users.models import User
from .models import Complaint, ComplaintSupport
from math import radians, sin, cos, sqrt, atan2
from django.db.models import Count
#citizen----------------------------------------------------------------------------------------------------------
def distance(lat1, lon1, lat2, lon2):
    R = 6371000

    dlat = radians(float(lat2) - float(lat1))
    dlon = radians(float(lon2) - float(lon1))

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(float(lat1)))
        * cos(radians(float(lat2)))
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c
class CreateComplaintView(CreateAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Complaint.objects.all()
    serializer_class=ComplaintSerializer
    
    
   
    def perform_create(self, serializer):

        lat = serializer.validated_data['latitude']
        lon = serializer.validated_data['longitude']
        category = serializer.validated_data['category']

        complaints = Complaint.objects.filter(
            category=category
        ).exclude(status='resolved')

        for complaint in complaints:

            dist = distance(
                lat,
                lon,
                complaint.latitude,
                complaint.longitude
            )

            if dist <= 100:
                raise ValidationError({
                    "duplicate": True,
                    "complaint_id": complaint.id,
                    "message": "Similar complaint already exists nearby"
                })

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
    
class DepartmentWorkers(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkerSerializer

    def get_queryset(self):
        return User.objects.filter(
            role='worker',
            department=self.request.user.department
        )
    
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


class SupportComplaintView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        complaint = Complaint.objects.get(pk=pk)

        support, created = ComplaintSupport.objects.get_or_create(
            complaint=complaint,
            user=request.user
        )

        if not created:
            return Response(
                {"message": "You already supported this complaint"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "message": "Complaint supported successfully"
        })
    

class PopularComplaints(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ComplaintSerializer

    def get_queryset(self):
        return Complaint.objects.annotate(
            support_count=Count('supports')
        ).order_by('-support_count')    
