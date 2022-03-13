from django.urls import path
from .views import addcontact

urlpatterns = [
    path('addcontact/',addcontact),
]