# Generated by Django 2.2.3 on 2019-07-19 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('blogManager', models.CharField(max_length=30)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('head', models.CharField(max_length=50)),
                ('button', models.CharField(max_length=20)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('link', models.URLField()),
                ('iconName', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]
