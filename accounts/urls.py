from django.urls import path
from django.contrib.auth.views import LoginView
from .views import register, dashboard, jobseeker_dashboard, employer_dashboard, logout_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('jobseeker/dashboard/', jobseeker_dashboard, name='jobseeker_dashboard'),
    path('employer/dashboard/', employer_dashboard, name='employer_dashboard'),

    path('logout/', logout_view, name='logout'),
]
