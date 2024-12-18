# Generated by Django 5.1.4 on 2024-12-16 16:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('background_colour', models.CharField(default='#007bff', max_length=7)),
                ('text_color', models.CharField(default='white', max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('feature_image', models.ImageField(blank=True, null=True, upload_to='blog/images')),
                ('excerpt', models.TextField(max_length=200)),
                ('content', models.TextField()),
                ('hashtags', models.CharField(help_text='Comma-separated hashtags', max_length=255)),
                ('meta_description', models.TextField(max_length=160)),
                ('meta_keywords', models.CharField(help_text='Comma-separated SEO keywords', max_length=255)),
                ('alt_text', models.CharField(help_text='Alt text for feature image', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.category')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
