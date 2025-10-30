from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'), 
    path('home/', views.home, name='home_page'),

    path('register/', views.register, name='register'),
    path('login/', views.login, name='user_login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    
    path('create_post/', views.create_post, name='create_post'),
    path('posts/', views.api_post_list, name='post-list'),
    path('posts/<int:id>/', views.api_post_detail, name='post-detail'),
]

extra_patterns = [
    path('register/', views.register, name='register'),
    path('create_post/', views.create_post, name='create_post'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/', views.home, name='home'),
]