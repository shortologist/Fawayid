# Generated by Django 2.2.3 on 2019-07-19 04:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import doc.utility


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auther', models.BooleanField(default=False)),
                ('about', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, upload_to=doc.utility.upload_profile_photo)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('postalCode', models.CharField(blank=True, max_length=20)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User Profile')),
            ],
        ),
    ]
