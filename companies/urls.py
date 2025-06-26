from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_company, name='create_company'),
     path('list/', views.company_list, name='company_list'),
]