from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def projects(request):
    return render(request, "project.html")

def about(request):
    return render(request, "about.html")

def error_404(request, exception):
    return render(request, "404.html", status=404)