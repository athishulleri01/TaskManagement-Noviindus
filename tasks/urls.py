from django.urls import path
from .views import UserTaskListAPIView, TaskStatusUpdateAPIView, TaskReportAPIView
from . import views
urlpatterns = [
    #< ----------------------------------superadmin-------------------------------------
    path('all_tasks_superuser/', views.task_list_view_superuser, name='task_list_superuser'),
    
    #< ----------------------------------admin-------------------------------------
    path('tasks/', UserTaskListAPIView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskStatusUpdateAPIView.as_view(), name='task-update'),
    path('tasks/create/', views.create_task_view, name='create_task'),
    path('all_tasks/', views.task_list_view, name='task_list'),
    path('tasks/<int:id>/edit/', views.edit_task_view, name='edit_task'),
    path('tasks/<int:task_id>/report/', views.task_report_view, name='task_report'),

]
