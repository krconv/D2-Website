from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    return render(request, "pages/MainWindow.html");

def links_page(request):
    return render(request, "pages/UsefulLinks.html");

def contact_page(request):
    return render(request, "pages/ContactUs.html");