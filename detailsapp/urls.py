from django.urls import path
from detailsapp import views

urlpatterns = [
    path('', views.fresher_view, name='fresher'),
    path('experienced/', views.experienced_view, name='experienced'),
    
    # Custom Admin URLs
    path('admin-panel/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('delete/<int:id>/', views.delete_applicant, name='delete_applicant'),
    path('submitted/', views.submit_success, name='submit_success'),
]
