from django.contrib import admin
from .models import Person, DeletedContacts


class PersonAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = Person.objects.filter(is_archived__in=[False]).all().order_by('-id')
        return queryset

    fields = ['user', 'name', 'email', 'phone1', 'phone2', 'phone3', 'is_archived', 'slug']
    list_display = ['name', 'email', 'phone1', 'phone2', 'phone3', 'slug', 'is_archived']
    list_per_page = 30
    readonly_fields = ['slug']
    search_fields = ['name__icontains']


class DeletedContactsAdmin(admin.ModelAdmin):
    fields = ['user', 'name', 'email', 'phone1', 'phone2', 'phone3', 'is_archived', 'slug']
    list_display = ['name', 'email', 'phone1', 'phone2', 'phone3', 'slug', 'is_archived']
    readonly_fields = ['slug']


admin.site.register(Person, PersonAdmin)
admin.site.register(DeletedContacts, DeletedContactsAdmin)

# Register your models here.
