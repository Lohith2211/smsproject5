from django.http import HttpResponse
# Httpresponse

def home(request):
    return HttpResponse("First Django Project")

def admin(request):
    return HttpResponse("I am in Admin Page")

def user(request):
    return HttpResponse("<b>I am in user page</b>")

