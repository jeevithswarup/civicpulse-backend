from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils.timezone import now
from rest_framework.generics import (
    CreateAPIView, ListAPIView, UpdateAPIView,
    DestroyAPIView, RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError
from .serializers import (
    ComplaintSerializer,
    AssignOfficerSerializer,
    UpdateComplaintStatusSerializer,
    AssignedWorkerSerializer,   # fixed name (was AssignedWorkerSerialializer)
    WorkerUpdateSerializer,
)
from users.serializers import WorkerSerializer
from users.models import User
from .models import Complaint, ComplaintSupport
from math import radians, sin, cos, sqrt, atan2
from django.db.models import Count


# ── helpers ──────────────────────────────────────────────────────────────────

def haversine(lat1, lon1, lat2, lon2):
    """Return distance in metres between two lat/lon points."""
    R = 6_371_000
    dlat = radians(float(lat2) - float(lat1))
    dlon = radians(float(lon2) - float(lon1))
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(float(lat1))) * cos(radians(float(lat2))) * sin(dlon / 2) ** 2
    )
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


# ── Citizen ───────────────────────────────────────────────────────────────────

class CreateComplaintView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer

    def perform_create(self, serializer):
        lat = serializer.validated_data['latitude']
        lon = serializer.validated_data['longitude']
        category = serializer.validated_data['category']

        nearby = Complaint.objects.filter(category=category).exclude(status='resolved')
        for complaint in nearby:
            if haversine(lat, lon, complaint.latitude, complaint.longitude) <= 100:
                raise ValidationError({
                    "duplicate": True,
                    "complaint_id": complaint.id,
                    "message": "A similar complaint already exists nearby.",
                })

        serializer.save(createdBy=self.request.user)


class MyComplaints(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ComplaintSerializer

    def get_queryset(self):
        return Complaint.objects.filter(createdBy=self.request.user).order_by('-created_at')


class UpdateComplaint(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ComplaintSerializer

    def get_queryset(self):
        return Complaint.objects.filter(createdBy=self.request.user)


class ComplaintDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ComplaintSerializer

    def get_queryset(self):
        return Complaint.objects.filter(createdBy=self.request.user)


class ComplaintDelete(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ComplaintSerializer

    def get_queryset(self):
        return Complaint.objects.filter(createdBy=self.request.user)


class CitizenDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        complaints = Complaint.objects.filter(createdBy=request.user)
        return Response({
            "my_complaints": complaints.count(),
            "resolved": complaints.filter(status="resolved").count(),
            "pending": complaints.filter(status="pending").count(),
        })


class SupportComplaintView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            complaint = Complaint.objects.get(pk=pk)
        except Complaint.DoesNotExist:
            return Response({"detail": "Complaint not found."}, status=status.HTTP_404_NOT_FOUND)

        _, created = ComplaintSupport.objects.get_or_create(
            complaint=complaint, user=request.user
        )
        if not created:
            return Response(
                {"detail": "You already supported this complaint."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"message": "Supported successfully."})


class PopularComplaints(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ComplaintSerializer

    def get_queryset(self):
        return Complaint.objects.annotate(
            total_supports=Count('supports')
        ).order_by('-total_supports')[:20]


class NearbyComplaints(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ComplaintSerializer

    def get_queryset(self):
        # Read lat/lon from query params sent by the frontend
        try:
            user_lat = float(self.request.query_params.get('lat', 0))
            user_lon = float(self.request.query_params.get('lon', 0))
        except (TypeError, ValueError):
            user_lat, user_lon = 0.0, 0.0

        # Radius in metres — 5km default
        radius = float(self.request.query_params.get('radius', 5000))

        complaints = Complaint.objects.exclude(status='resolved')

        # If no valid coords given, just return latest 50
        if user_lat == 0.0 and user_lon == 0.0:
            return complaints.order_by('-created_at')[:50]

        # Filter using Haversine — calculate in Python since SQLite
        # doesn't have native geo functions
        nearby = []
        for complaint in complaints:
            try:
                dist = haversine(
                    user_lat, user_lon,
                    float(complaint.latitude),
                    float(complaint.longitude)
                )
                if dist <= radius:
                    nearby.append(complaint.id)
            except Exception:
                continue

        return Complaint.objects.filter(
            id__in=nearby
        ).order_by('-created_at')[:50]


# ── Officer ───────────────────────────────────────────────────────────────────

class OfficerDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        complaints = Complaint.objects.filter(assignedOfficer=request.user)
        return Response({
            "total": complaints.count(),
            "pending": complaints.filter(status="pending").count(),
            "assigned": complaints.filter(status="assigned").count(),
            "in_progress": complaints.filter(status="in_progress").count(),
            "resolved": complaints.filter(status="resolved").count(),
        })


class AssignedOfficerView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AssignOfficerSerializer
    queryset = Complaint.objects.all()

    def perform_update(self, serializer):
        officer = serializer.validated_data['assignedOfficer']
        if officer.role != 'officer':
            raise ValidationError("Selected user is not an officer.")
        serializer.save(status='assigned')


class ListOfficierComplaints(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ComplaintSerializer

    def get_queryset(self):
        return Complaint.objects.filter(assignedOfficer=self.request.user).order_by('-created_at')


class OfficerComplaintDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ComplaintSerializer

    def get_queryset(self):
        return Complaint.objects.filter(assignedOfficer=self.request.user)


class UpdateComplaintStatus(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateComplaintStatusSerializer

    def get_queryset(self):
        return Complaint.objects.filter(assignedOfficer=self.request.user)

    def perform_update(self, serializer):
        complaint = serializer.save()
        if complaint.status == "resolved":
            complaint.resolved_at = now()
            complaint.save()


class DepartmentWorkers(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkerSerializer

    def get_queryset(self):
        return User.objects.filter(
            role='worker',
            department=self.request.user.department,
        )


# ── Worker ────────────────────────────────────────────────────────────────────

class WorkerDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        complaints = Complaint.objects.filter(assignedWorker=request.user)
        return Response({
            "assigned": complaints.filter(status="assigned").count(),
            "in_progress": complaints.filter(status="in_progress").count(),
            "resolved": complaints.filter(status="resolved").count(),
        })


class AssignedWorkerView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AssignedWorkerSerializer   # fixed name
    queryset = Complaint.objects.all()

    def perform_update(self, serializer):
        worker = serializer.validated_data['assignedWorker']
        if worker.role != 'worker':
            raise ValidationError("Selected user is not a worker.")
        if worker.department != self.request.user.department:
            raise ValidationError("Worker must belong to your department.")
        serializer.save(status='in_progress')


class AssignedWorkerComplaints(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ComplaintSerializer

    def get_queryset(self):
        return Complaint.objects.filter(assignedWorker=self.request.user).order_by('-created_at')


class WorkerUpdateComplaint(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkerUpdateSerializer

    def get_queryset(self):
        return Complaint.objects.filter(assignedWorker=self.request.user)

    def perform_update(self, serializer):
        complaint = serializer.save()
        if complaint.status == 'resolved':
            complaint.resolved_at = now()
            complaint.save()


class WorkerComplaintDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ComplaintSerializer

    def get_queryset(self):
        return Complaint.objects.filter(assignedWorker=self.request.user)


# ── Admin ─────────────────────────────────────────────────────────────────────

class AdminDashboard(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({
            "total_complaints": Complaint.objects.count(),
            "total_citizens":   User.objects.filter(role='citizen').count(),
            "total_officers":   User.objects.filter(role='officer').count(),
            "total_workers":    User.objects.filter(role='worker').count(),
            "resolved":         Complaint.objects.filter(status='resolved').count(),
            "pending":          Complaint.objects.filter(status='pending').count(),
        })
