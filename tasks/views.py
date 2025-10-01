from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task
from .serializers import TaskSerializer, TaskStatusUpdateSerializer
from django.contrib.auth.decorators import login_required
from core_apps.users.models import User
from django.http import HttpResponseForbidden



# superuser can view task report and working hours
class TaskReportAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_superuser and not request.user.is_staff:
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)

        if task.status != 'completed':
            return Response({'error': 'Task not completed'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'completion_report': task.completion_report,
            'worked_hours': task.worked_hours
        })



# admin can create task
@login_required
def create_task_view(request):
    if request.method == 'POST' and request.user.role in ['admin', 'superadmin']:
        Task.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            assigned_to_id=request.POST['assigned_to'],  
            due_date=request.POST['due_date'],
            status='pending'
        )

        return redirect('task_list')
    
    users = User.objects.filter(role='user')
    return render(request, 'adminside/tasks/task_page.html', {'users': users})


# admin can view all tasks
@login_required
def task_list_view(request):
    tasks = Task.objects.all()
    users = User.objects.filter(role="user")
    return render(request, 'adminside/tasks/list_tasks.html', {'tasks': tasks, 'users' :users})


# superuser can view all tasks
@login_required
def task_list_view_superuser(request):
    tasks = Task.objects.all()
    users = User.objects.filter(role="user")
    return render(request, 'adminside/tasks/list_tasks_superuser.html', {'tasks': tasks, 'users' :users})

# asigned user can list their task 
class UserTaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)


class TaskStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
        
        
@login_required
def edit_task_view(request, id):
    task = get_object_or_404(Task, id=id) 

    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.assigned_to_id = get_object_or_404(User, pk=request.POST['assigned_to'])
        task.due_date = request.POST['due_date']
        task.status = request.POST['status']
        task.save()
        return redirect('task_list') 

    users = User.objects.filter(role='user')
    return render(request, 'adminside/tasks/edit_task.html', {'task': task, 'users': users})



@login_required
def task_report_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Only superadmins or admins can view reports
    if request.user.role not in ['admin', 'superadmin']:
        return HttpResponseForbidden("You don't have permission to view this report.")

    if task.status != 'completed':
        return HttpResponseForbidden("Report is only available for completed tasks.")

    return render(request, 'adminside/tasks/task_report.html', {'task': task})