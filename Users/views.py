from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check if the user is a superuser and redirect to the admin interface
            if user.is_superuser:
                return redirect('/admin/')  # Redirect to the Django admin interface
            
             # Check if the user is an admin and redirect to the dashboard
            else:
                return redirect('dashboard:index')  # Redirect to the dashboard homepage

        else:
            messages.error(request, "You do not have the right permissions to access this system.")
            return redirect('users:login')  # Use the correct namespace

        # else:
        #     messages.error(request, "Invalid email or password.")
        #     return redirect('users:login')  # Use the correct namespace

    return render(request, 'users/sign_in.html')  # Render the sign-in template

# def loged_user(request, user):
#     if user is not None:
#          user = request.user
#     return render( 'components/sidebar.html',{'user':user})