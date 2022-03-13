from django.urls import path
from . import views

urlpatterns = [
    path('', views.contactList),
    path('details/<slug:slug>/', views.details),
    path('addcontact/',views.addcontact),

    # api
    path('contact_list_api/', views.contact_list_api.as_view()),
    path('details_api/<slug:slug>/', views.DetailsApi.as_view()),
    path('contact_edit_api/<slug:slug>/', views.contact_edit_api.as_view()),
    path('addcontact_api/',views.Add_contact_api.as_view()),
]

