from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    return render(request, "pages/Home.html");

def links_page(request):
    return render(request, "pages/UsefulLinks.html");

def meet_us_page(request):
    return render(request, "pages/MeetUs.html");

def ctf_page(request):
    return render(request, "pages/CaptureTheFlag.html");

def contact_page(request):
    return render(request, "pages/ContactUs.html");