from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from core_apps.users.models import User 
from django.contrib.auth import logout as django_logout
from rest_framework_simplejwt.tokens import RefreshToken 
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
    
@never_cache
@login_required(login_url='admin_login')
def DashBoard(request):
    if request.user.role not in ['admin', 'superadmin']:
        return redirect('admin_login')  # prevent unauthorized access
    if request.user.role == "superadmin":
        return render(request, 'adminside/dashboard/superadmin_index.html', {'user': request.user})
    return render(request, 'adminside/dashboard/admin_index.html', {'user': request.user})
    
    

@never_cache
def admin_login_view(request):
    if request.user.is_authenticated and request.user.role in ['admin', 'superadmin']:
        return redirect('superuser_dashboard')  # Use the name of your dashboard URL pattern

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.role in ['admin', 'superadmin']:
            login(request, user)
            
            tokens = get_tokens_for_user(user)
            print("accecc   : ",tokens['access'])
            if user.role == "superadmin":
                response = redirect('superuser_dashboard')
            else:
                response = redirect('admin_dashboard')
            # Set tokens in cookies (HttpOnly for security)
            response.set_cookie('access_token', tokens['access'], httponly=False)
            response.set_cookie('refresh_token', tokens['refresh'], httponly=False)

            return response

        return render(request, 'adminside/admin_login.html', {'error': 'Invalid credentials or not authorized.'})

    return render(request, 'adminside/admin_login.html')


 # Superuser register a new user
@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        name = request.POST.get("name")
        email = request.POST.get("email")
        role = request.POST.get("role")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        re_password = request.POST.get("re_password")
        if not all([username, name, email, mobile, password, re_password]):
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        if password != re_password:
            return JsonResponse({'error': 'Passwords do not match.'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists.'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already in use.'}, status=400)
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name,
            mobile = mobile,
            role = role
        )
        
        users = User.objects.filter(role="user")
        return render(request, 'adminside/users/admin_details.html', {'users': users})

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)


# logout 
def logout_view(request):
    logout(request)
    response = redirect('admin_login')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response


# superAmin view the user details
def list_admin_users(request):
    admin_users = User.objects.filter(role="admin")
    return render(request, 'adminside/users/admin_details.html', {'users': admin_users})


# superadmin can block user
def UserBlock(request, user_id):
    user = User.objects.get(id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
        
        users = User.objects.filter(role=user.role).order_by('id')
        context = {
            'users': users
        }
        if user.role == "admin":
            return render(request, 'adminside/users/admin_details.html', context)
        elif user.role == "user":
            return render(request, 'adminside/users/users_details.html', context)
    else:
        user.is_active = True
        user.save()
        users = User.objects.filter(role=user.role).order_by('id')
        context = {
            'users': users
        }
        if user.role == "admin":
            return render(request, 'adminside/users/admin_details.html', context)
        elif user.role == "user":
            return render(request, 'adminside/users/users_details.html', context)
 
 
#  admin dashboard 
def admin_dashboard(request):
    return render(request, 'adminside/dashboard/admin_index.html', {'user': request.user})


# superAmin view the user details
def list_users(request):
    users = User.objects.filter(role="user")
    return render(request, 'adminside/users/users_details.html', {'users': users})


# verifyng the superuser
def is_superadmin(user):
    return user.is_authenticated and user.role == 'superadmin'


# superuser delete admin
@login_required
@user_passes_test(is_superadmin)
def delete_admin(request, user_id):
    admin_user = get_object_or_404(User, id=user_id, role='admin')
    if admin_user:
        admin_user.delete()
    
    return redirect('admin_details') 


# superuser delete user
@login_required
@user_passes_test(is_superadmin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id, role='user')
    
    if user:
        user.delete()
        

    return redirect('user_details') 


# superuser can update user role
@require_POST
def update_user_role(request, user_id):
    user = get_object_or_404(User, id=user_id)
    new_role = request.POST.get('role')
    
    if new_role in ['user', 'admin']:
        user.role = new_role
        user.save()
    
    return redirect('user_details') 


# superuser can update admin role
@require_POST
def update_admin_role(request, user_id):
    user = get_object_or_404(User, id=user_id)
    new_role = request.POST.get('role')
    
    if new_role in ['user', 'admin']:
        user.role = new_role
        user.save()
    
    return redirect('admin_details') 



def list_admin_all_users(request):
    users = User.objects.filter(role="user")
    return render(request, 'adminside/users/users_details_for_admin.html', {'users': users})