from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from user.models import CustomUser
from .models import Profile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=CustomUser)
def deactivate_profile_on_user_deactivate(sender, instance, **kwargs):
    if not instance.is_active:
        profile = instance.profile
        profile.is_active = False
        profile.save()


@receiver(post_delete, sender=CustomUser)
def delete_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.delete()
