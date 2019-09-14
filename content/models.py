from django.db import models
from doc.utility import upload_header_image


class About(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    address = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    email = models.EmailField()
    blogManager = models.CharField(max_length=30)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Header(models.Model):
    title = models.CharField(max_length=30)
    head = models.CharField(max_length=50)
    button = models.CharField(max_length=20)
    active = models.BooleanField(default=False)
    image = models.ImageField(upload_to=upload_header_image, blank=True)
    def __str__(self):
        return self.title


class SocialLink(models.Model):
    title = models.CharField(max_length=20)
    link = models.URLField()
    iconName = models.CharField(max_length=50)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title