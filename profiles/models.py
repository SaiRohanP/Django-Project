from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        related_name = "profile"
    ) 

    def __str__(self):
        return self.user.username

#receives signal if a User is created(saved).
@receiver(post_save, sender=User)

def create_user_profile(sender,instance,created,**kwargs):
    #Create a Profile object whenever a User is created.
    if created:
        Profile.objects.create(user=instance)