from django.contrib import admin
from django.urls import path, include
from .views import details, DetailsApi

urlpatterns = [
    path('details/<slug:slug>/', details),
    #api
    path('details_api/<slug:slug>/', DetailsApi.as_view()),
]
