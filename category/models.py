from django.db import models
from doc.utility import upload_category_image, generate_slug
from django.db.models.signals import pre_save


class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to=upload_category_image, blank=True)
    active = models.BooleanField(default=False)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


def assign_slug(sender, instance, *args, **kwargs):
    if instance.slug == '':
        instance.slug = generate_slug(instance, instance.title)


pre_save.connect(assign_slug, sender=Category)
