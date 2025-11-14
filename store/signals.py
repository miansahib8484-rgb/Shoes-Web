from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'userprofile'):
            instance.userprofile.save()



@receiver(user_logged_in)
def user_login_check(sender, request, user, **kwargs):
 
    if user.is_superuser:
        return

    if not hasattr(user, 'userprofile') or not user.userprofile.can_login:
        logout(request)
        return redirect('/')


