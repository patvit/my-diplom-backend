from django.db import models

import os
import math
import logging

# Create your models here.

from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.conf import settings

from dotenv import load_dotenv

from accounts.models import CustomUser

load_dotenv()

logger = logging.getLogger(__name__)


def ensure_unique_filename(user_folder, filename):
    new_filepath = os.path.join(user_folder, filename)
    if Document.objects.filter(file=new_filepath):
        filename = generate_unique_name(user_folder, filename)
    return filename


def generate_unique_name(user_folder, filename):
    count = 0
    file_root, file_ext = os.path.splitext(filename)
    while Document.objects.filter(file=os.path.join(user_folder, filename)):
        count += 1
        filename = f'{file_root}_{count}{file_ext}'
    return filename


def format_size(size_bytes):
    size_units = ('B', 'KB', 'MB', 'GB')
    i = int(math.floor(math.log(size_bytes, 1024)))
    s = round(size_bytes / math.pow(1024, i), 2)
    return f'{s} {size_units[i]}'


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(null=True, verbose_name='Stored File')
    filename = models.CharField(max_length=255, null=True, default='')
    description = models.TextField(null=True, default='')
    size = models.CharField(null=True, default='')
    share_link = models.CharField(max_length=100, null=True, default='')
    upload_datetime = models.DateTimeField(default=timezone.now)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1, related_name='document2customuser')

    def save(self, *args, **kwargs):
        user_folder = self.uploaded_by.username
        hash_link = hash(self.upload_datetime)

        if self.id:
            logger.info(
                f"Updating document with id='{self.id}' and filename='{self.filename}' initiated by {self.uploaded_by}.")
            old_full_filepath = self.file.path
            new_full_filepath = os.path.join(settings.MEDIA_ROOT, user_folder, self.filename)
            self.file.name = os.path.join(user_folder, self.filename)
            os.rename(old_full_filepath, new_full_filepath)
        else:
            file_root, file_ext = os.path.splitext(self.file.name)

            if self.filename:
                self.filename = ensure_unique_filename(user_folder, f'{self.filename}{file_ext}')
                self.file.name = os.path.join(user_folder, self.filename)
            else:
                self.filename = self.file.name
                self.file.name = os.path.join(user_folder, f'{hash_link}{file_ext}')

            self.share_link = f'{os.getenv("REACT_APP_API_URL")}/s/{hash_link}'
            self.size = format_size(self.file.size)

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.file.name)


@receiver(models.signals.post_delete, sender=Document)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)