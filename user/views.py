from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer, PasswordResetConfirmSerializer, PasswordResetRequestSerializer
from django.contrib.auth import authenticate
from profiles.models import Profile


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class LoginViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(
            request, email=email, password=password)

        if user is None:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            profile = Profile.objects.get(user=user)
            profile_slug_id = profile.slug_id
        except Profile.DoesNotExist:
            profile_slug_id = None

        refresh = RefreshToken.for_user(user)

        response_data = {
            "user": UserSerializer(user).data,
            "profile_id": profile_slug_id,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(response_data, status=status.HTTP_200_OK)


class PasswordResetRequestViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password reset link has been sent if the email is registered."}, status=status.HTTP_200_OK)


class PasswordResetConfirmViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
