from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from departments.models import Department

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # 'role' is intentionally excluded — all self-registered users are citizens
        fields = [
            'username',
            'email',
            'phone',
            'preferred_language',
            'password',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        # Force role to citizen for all public registrations
        user = User(**validated_data, role='citizen')
        user.set_password(password)
        user.save()
        return user

    
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self, data):

        user=authenticate(
            username=data["username"],
            password=data["password"]
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        
        data["user"]=user
        return data
class CreateOfficerSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)

    class Meta:
         model=User
         fields=[
             'username',
             'email',
             'phone',
            'password',
            'department',
         ]
    def  create(self, validated_data):
        password=validated_data.pop('password')
        user = User(**validated_data,role='officer')
        user.set_password(password)
        user.save()

        return user


class CreateWorkerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone',
            'password'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User(
            **validated_data,
            role='worker',
            department=self.context['request'].user.department
        )

        user.set_password(password)
        user.save()

        return user
    
class WorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'phone',
            'department'
        ]    