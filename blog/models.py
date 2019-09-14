from django.db import models
from django.contrib.auth.models import User
from doc.utility import upload_post_image, post_status
from django.db.models.signals import pre_save
from doc.utility import generate_slug
from django.shortcuts import reverse
from fawayid.category.models import Category


class PostManager(models.Manager):
    def year_archive(self, year):
        return self.get_queryset().filter(pub_date__year=year)

    def year_month_archive(self, year, month):
        return self.get_queryset().filter(pub_date__year=year,
                                          pub_date__month=month)


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=upload_post_image, blank=True)
    publishDate = models.DateTimeField(auto_now_add=True)
    modifyDate = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=9, choices=post_status,
                             default='draft')
    slug = models.SlugField(unique=True, blank=True)
    objects = PostManager()

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])

    def __str__(self):
        return self.title


def assign_slug(sender, instance, *args, **kwargs):
    if instance.slug == '':
        instance.slug = generate_slug(instance, instance.title)


pre_save.connect(assign_slug, sender=Post)


class Viewer(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    viewer_ip = models.GenericIPAddressField()
    date_view = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title


class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class SavedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    saved_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title