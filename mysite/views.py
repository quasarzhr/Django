from django.http import HttpResponse

def hello(request):
    """For /hello/ URL"""
    return HttpResponse("Hello Django")

def logic_view(request):
    """For /logic/?status=ok or fail"""
    status = request.GET.get("status")
    if status == "ok":
        return HttpResponse("Logic OK")
    return HttpResponse("Logic Fail", status=400)

def home(request):
    """For /home/ URL"""
    return HttpResponse("My Home Page")
