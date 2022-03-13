from django.urls import path
from . import views

urlpatterns = [
    path('addcontact/',views.addcontact),
    path('addcontact_api/',views.Add_contact_api.as_view()),
]