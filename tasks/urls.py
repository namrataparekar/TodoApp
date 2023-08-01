from . import views
from django.urls import path

from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views
from .views import UserView

app_name = 'tasks'

urlpatterns = [
     path('',views.home,name="home"),
     path('list/',views.index, name="list"),
     path('update_task/<str:pk>/',views.update_task, name="update_task"),
     path('delete/<str:pk>/',views.deleteTask, name="delete"),
     path('login/', views.loginView, name="login"),
     path('admindashboard/',views.admindashboard, name="admindashboard"),
     path('logout/', auth_views.LogoutView.as_view(next_page='/login'), name='logout'),
     path('profile/',login_required(UserView.as_view()),name = 'profile'),
     path('signup/', views.signup, name='signup'),
    
]





# urlpatterns = [
#      path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
#      path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login'), name='logout'),
#      path('profile/',  login_required(UserView.as_view()), name='profile'),
#      path('signup/', signup, name='signup')
# ]