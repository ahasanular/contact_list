import secrets

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_archived = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

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