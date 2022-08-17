import secrets

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# import for QR code

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


# Create your models here.
class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_archived = models.BooleanField(default=False)

    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)

    phone1 = models.CharField(max_length=15, null=True, blank=True)
    phone2 = models.CharField(max_length=15, null=True, blank=True)
    phone3 = models.CharField(max_length=15, null=True, blank=True)

    slug = models.SlugField(max_length=255, unique=True)
    def __str__(self):
        return self.name


class DeletedContacts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_archived = models.BooleanField(default=False)

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, null=True, blank=True)

    phone1 = models.CharField(max_length=15)
    phone2 = models.CharField(max_length=15, null=True, blank=True)
    phone3 = models.CharField(max_length=15, null=True, blank=True)

    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name
