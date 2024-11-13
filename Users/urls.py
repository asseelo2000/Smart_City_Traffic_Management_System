from django.urls import include, path
from . import views
import Dashboard
from Dashboard.views import index
app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Ensure this URL pattern exists
    path('dashboard/', index, name='dashboard' ),  # Dashboard URLs

]