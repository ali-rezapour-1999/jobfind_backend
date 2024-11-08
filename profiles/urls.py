from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, WorkHistoryViewSet, EducationViewSet, SkillViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'work-history', WorkHistoryViewSet)
router.register(r'education', EducationViewSet)
router.register(r'skills', SkillViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
