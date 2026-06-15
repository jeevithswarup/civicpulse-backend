from rest_framework import serializers
from .models import Complaint


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


class AssignedWorkerSerialializer(serializers.ModelSerializer):

   class Meta:
      model=Complaint
      fiels=[
         'assignedWorker'
      ]