from django.contrib import admin
from django.urls import path, include
from .views import home

admin.site.site_header = "Kabir_Admin"
admin.site.site_title = "Kabir Admin Portal"
admin.site.index_title = "Welcome to Kabir Portal"

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('registration/', include('registration.urls')),
    path('contacts/', include('contacts.urls')),
]
