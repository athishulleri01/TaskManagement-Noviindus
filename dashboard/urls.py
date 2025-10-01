from django.urls import path
from . import views
from uuid import UUID

urlpatterns = [
    #< ----------------------------------superadmin-------------------------------------
    path('super_admin_dash/', views.DashBoard, name="superuser_dashboard"),
    path('admin_login', views.admin_login_view, name="admin_login"),
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout_view, name='admin_logout'),
    path('admin_details/', views.list_admin_users, name="admin_details"),
    path('user_details/', views.list_users, name="user_details"),
    path('block_user/<uuid:user_id>/', views.UserBlock, name="block_user"),
    path('delete_admin/<uuid:user_id>/', views.delete_admin, name='delete_admin'),
    path('delete_user/<uuid:user_id>/', views.delete_user, name='delete_user'),
    path('update-role/<uuid:user_id>/', views.update_user_role, name='update_user_role'),
    path('update-admin-role/<uuid:user_id>/', views.update_admin_role, name='update_admin_role'),
    
    #<------------------------------------admin----------------------------------------------
    path('admin_dash/', views.admin_dashboard, name="admin_dashboard"),
    path('user_details_admin/', views.list_admin_all_users, name="user_details_admin"),
    
    

]