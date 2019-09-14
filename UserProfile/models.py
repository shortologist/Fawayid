from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from doc.utility import upload_profile_photo
from django.db.models.signals import post_save
from doc.utility import generate_slug


class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE,related_name="profile",verbose_name=_('User Profile'))
    auther = models.BooleanField(default=False)
    about = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to=upload_profile_photo, blank=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    postalCode = models.CharField(max_length=20, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.slug = generate_slug(profile, profile.user.username)
        profile.photo = 'profile/default.jpg'
        profile.save()


post_save.connect(create_user_profile, sender=User)