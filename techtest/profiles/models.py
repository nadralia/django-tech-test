from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.reverse import reverse

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username



def user_post_save_reciever(*args, **kwargs):
    created = kwargs.get("created")
    user = kwargs.get("instance")
    if created:
        Profile.objects.get_or_create(user=user,
                                      username=user.username)


post_save.connect(user_post_save_reciever, sender=settings.AUTH_USER_MODEL)

