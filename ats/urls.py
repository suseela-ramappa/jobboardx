from django.urls import path
from . import views

urlpatterns = [
    path('analyzer/', views.ats_analyzer_view, name='ats_analyzer'),
]
