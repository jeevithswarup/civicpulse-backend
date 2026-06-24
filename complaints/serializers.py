from rest_framework import serializers
from .models import Complaint,ComplaintSupport


class ComplaintSerializer(serializers.ModelSerializer):
   class Meta:
      model=Complaint
      fields = [
      'title',
      'description',
      'category',
      'address',
      'latitude',
      'longitude',
      'image',
      'priority',
  ]
      
#officer-----------------------------------------------------------------------------------------------------      
class AssignOfficerSerializer(serializers.ModelSerializer):

   class Meta:
      model=Complaint
      fields=[
         'assignedOfficer'
      ]

class UpdateComplaintStatusSerializer(serializers.ModelSerializer):
   
   class Meta:
      model=Complaint
      fields=[
         'status'
      ]


#Worker----------------------------------------------------------------------------------------------------------
class AssignedWorkerSerialializer(serializers.ModelSerializer):

   class Meta:
      model=Complaint
      fields=[
         'assignedWorker'
      ]

class WorkerUpdateSerializer(serializers.ModelSerializer):

   class Meta:
      modle=Complaint
      fields=[
         'latitude',
         'longitude',
         'resolution_image',
         'status',
         'worker_notes',
      ]
      

class ComplaintSerializer(serializers.ModelSerializer):

    support_count = serializers.SerializerMethodField()

    class Meta:
        model = Complaint
        fields = '__all__'

    def get_support_count(self, obj):
        return obj.supports.count()

    