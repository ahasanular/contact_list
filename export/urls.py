from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # api
    path('contacts_export/<slug:slug>/', views.export_contact)
]