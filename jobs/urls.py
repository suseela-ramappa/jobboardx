from django.urls import path
from . import views
from jobs.views import home,job_detail,view_applications

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('home/', views.home, name='home'),
    path('post_job/', views.post_job, name='post_job'),
    path('my_applications/', views.my_applications, name='my_applications'),
    path('employer/manage_jobs/', views.manage_jobs, name='manage_jobs'),
    path('jobs/<int:pk>/', job_detail, name='job_detail'),
    path('jobs/<int:job_id>/applications/', view_applications, name='view_applications'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('applications/<int:application_id>/update/<str:status>/', views.update_application_status, name='update_application_status')
 
]
