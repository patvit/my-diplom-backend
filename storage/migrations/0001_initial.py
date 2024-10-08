# Generated by Django 4.2.15 on 2024-08-14 08:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(null=True, upload_to='', verbose_name='Stored File')),
                ('filename', models.CharField(default='', max_length=255, null=True)),
                ('description', models.TextField(default='', null=True)),
                ('size', models.CharField(default='', null=True)),
                ('share_link', models.CharField(default='', max_length=100, null=True)),
                ('upload_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('uploaded_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
