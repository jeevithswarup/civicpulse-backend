from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from .models import User
from rest_framework.exceptions import PermissionDenied
from .serializers import RegisterSerializer,CreateOfficerSerializer,CreateWorkerSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # Flatten errors into a single readable message for the frontend
            errors = serializer.errors
            # username already taken is the most common case
            if 'username' in errors:
                msg = f"Username: {errors['username'][0]}"
            elif 'phone' in errors:
                msg = f"Phone: {errors['phone'][0]}"
            elif 'email' in errors:
                msg = f"Email: {errors['email'][0]}"
            else:
                msg = list(errors.values())[0][0] if errors else "Registration failed."
            return Response({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "username": user.username,
                "role": user.role,
            })

        # Return a clean `detail` key so the frontend client can read it directly
        return Response(
            {"detail": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED
        )


class ProfileView(APIView):

    permission_classes=[IsAuthenticated]

    def get(self,request):
        return Response({
            "id":request.user.id,
            "username":request.user.username,
            "email":request.user.email,
            "phone":request.user.phone,
            "role":request.user.role,
            "preferred_language":request.user.preferred_language
        })



class CreateOfficerView(CreateAPIView):
    permission_classes=[IsAdminUser]
    serializer_class=CreateOfficerSerializer
    queryset=User.objects.all()


class CreateWorkerView(CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CreateWorkerSerializer
    queryset=User.objects.all()

    def perform_create(self, serializer):
        if self.request.user.role != "officer":
            raise PermissionDenied(
                "Only officers can create workers."
            )

        serializer.save()