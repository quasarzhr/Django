from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from . import views

from app import views as app_views

def home(request):
    return HttpResponse("Django is running successfully!")

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include(('app.urls', 'app'), namespace='app')),
    
    path('hello/', views.hello),
    path('logic/', views.logic_view),
    path('blog/', include('blog.urls')),
]

urlpatterns += [
    path('home/', app_views.home, name='home'),
    path('register/', app_views.register, name='register'),
    path('dashboard/', app_views.dashboard, name='dashboard'),
    path('create_post/', app_views.create_post, name='create_post'),
]