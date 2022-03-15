from django.contrib import admin
from .models import Person

class PersonAdmin(admin.ModelAdmin):
    fields = ['user', 'name', 'email', 'phone', 'is_archived', 'slug', 'qr_code']
    list_display = ['name', 'email', 'phone', 'slug', 'is_archived', 'qr_code']
    readonly_fields = ['slug', 'qr_code']

admin.site.register(Person, PersonAdmin)


# Register your models here.
