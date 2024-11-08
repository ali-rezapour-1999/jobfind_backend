from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, LoginViewSet, PasswordResetRequestViewSet, PasswordResetConfirmViewSet

router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'password-reset', PasswordResetRequestViewSet,
                basename='password-reset-request')
router.register(r'password-reset-confirm',
                PasswordResetConfirmViewSet, basename='password-reset-confirm')

urlpatterns = [
    path('', include(router.urls)),
]
