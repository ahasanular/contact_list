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
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15)
    slug = models.SlugField(max_length=255, unique=True)
    qr_code = models.ImageField(upload_to='qr_codes', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            person_exists = Person.objects.filter(slug=slug).exists()
            if person_exists:
                hexa = secrets.token_hex(10)
                self.slug = slug + "-AmRjZe798653-" + hexa
            else:
                self.slug = slug
            super(Person, self).save(*args, **kwargs)
        else:
            super(Person, self).save(*args, **kwargs)

        qr_code_picture = qrcode.make("Name : "+self.name+"\nPhone : "+self.phone+"\nEmail : "+self.email)
        canvas = Image.new('RGB', (720, 720), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qr_code_picture)
        qr_code_name = f'qr_code-{self.name}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(qr_code_name, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

