from rest_framework import serializers
from .models import Complaint, ComplaintSupport


class ComplaintSerializer(serializers.ModelSerializer):
    """Main serializer — used for create, list, retrieve."""
    support_count = serializers.SerializerMethodField()

    class Meta:
        model = Complaint
        fields = [
            'id',
            'complaintID',
            'title',
            'description',
            'category',
            'address',
            'latitude',
            'longitude',
            'resolution_image',   # correct field name (was 'image' — bug fixed)
            'worker_notes',
            'status',
            'priority',
            'support_count',
            'createdBy',
            'assignedOfficer',
            'assignedWorker',
            'department',
            'created_at',
            'updated_at',
            'resolved_at',
        ]
        read_only_fields = ['id', 'complaintID', 'createdBy', 'created_at', 'updated_at']

    def get_support_count(self, obj):
        return obj.supports.count()


# Officer: assign an officer to a complaint
class AssignOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['assignedOfficer']


# Officer: update complaint status
class UpdateComplaintStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['status']


# Officer: assign a worker to a complaint
class AssignedWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint        # was 'modle' (typo) — bug fixed
        fields = ['assignedWorker']


# Worker: update their own progress on a complaint
class WorkerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint        # was 'modle' (typo) — bug fixed
        fields = [
            'resolution_image',
            'status',
            'worker_notes',
        ]
