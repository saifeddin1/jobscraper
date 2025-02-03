from django.urls import path
from . import views

urlpatterns = [
    path("", views.job_list, name="job_list"),
    path("job/<int:job_id>/", views.job_detail, name="job_detail"),

    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('toggle-favorite/<int:job_id>/',
         views.toggle_favorite, name='toggle_favorite'),
    path('saved_jobs/', views.saved_jobs_view, name='saved_jobs'),
    path("settings/", views.settings_view, name="settings"),


]
