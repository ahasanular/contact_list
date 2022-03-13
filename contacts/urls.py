from django.urls import path
from . import views

urlpatterns = [
    path('', views.contactList),
    # path('details', views.),

    # api
    path('contact_list_api/', views.contact_list_api.as_view()),
    # path('contact_edit_api/', views.contact_edit_api.as_view()),
]
