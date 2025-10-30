from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import Post

def register(request):
    """Simple registration view for integration test."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        if username and password:
            User.objects.create_user(username=username, password=password)
            return redirect('app:user_login')
    return HttpResponse("Register page loaded")

def login(request):
    """Placeholder login view for testing."""
    return HttpResponse("Login page")

def logout(request):
    """Placeholder logout view for testing."""
    return HttpResponse("Logout successful")

def create_post(request):
    """Placeholder create_post view for testing error handling."""
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        if not title:
            return HttpResponse("Error: title is required", status=400)
        Post.objects.create(title=title, content=body or "")
        return HttpResponse(f"Post created: {title}")
    return HttpResponse("Create post page")

@login_required(login_url='/login/')
def dashboard(request):
    """Dashboard page — requires login to access."""
    return HttpResponse("Dashboard (protected area)")

def index(request):
    """Homepage."""
    return HttpResponse("Welcome to my Django app!")

def home(request):
    context = {"message": "Welcome to Django Testing"}
    return render(request, "home.html", context)

def api_post_list(request):
    data = list(Post.objects.values("id", "title", "content"))
    return JsonResponse(data, safe=False)

def api_post_detail(request, id):
    try:
        post = Post.objects.get(pk=id)
        return JsonResponse({"id": post.id, "title": post.title, "content": post.content})
    except Post.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)