from django.contrib import admin
from .models import Person

class PersonAdmin(admin.ModelAdmin):
    fields = ['user', 'name', 'email', 'phone', 'is_archived', 'slug']
    list_display = ['name', 'email', 'phone', 'slug', 'is_archived']
    readonly_fields = ['slug']

admin.site.register(Person, PersonAdmin)


# Register your models here.
