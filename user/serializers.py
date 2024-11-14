from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'slug_id')
        read_only_fields = ('slug_id',)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.CharField()

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
            self.context['user'] = user
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                "User with this email does not exist.")
        return value

    def save(self):
        user = self.context['user']
        token_generator = PasswordResetTokenGenerator()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        reset_link = f"#####/{uid}/{token}/"

        send_mail(
            subject="Password Reset Request",
            message=f"Use the following link to reset your password: {
                reset_link}",
            from_email='#####',
            recipient_list=[user.email],
        )
        return uid, token


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            uid = attrs.get('uid')
            token = attrs.get('token')
            user_id = force_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError("Invalid token or user ID.")

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            raise serializers.ValidationError("Token is invalid or expired.")

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user
