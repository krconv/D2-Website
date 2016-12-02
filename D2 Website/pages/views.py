from datetime import datetime
import mcstatus

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from d2 import settings
from . import models
from . import forms

"""
Common contexts
"""
def base_context(request):
    "The context required for the base template."
    context = {
        'website_title' : settings.WEBSITE_TITLE,
    }
    return context;

def minecraft_context(request):
    "Gets information about the server's address, status and player count."
    context = {}
    status = models.MinecraftServerPing.get_latest_status()
    if status:
        context['status'] = status.status
        context['is_online'] = status.is_online
        if (status.how_long_ago().seconds < 60):
            context['secs_ago'] = (int) (status.how_long_ago().seconds)
        else:
            context['mins_ago'] = (int) (status.how_long_ago().seconds / 60)
        if request.user.has_perm('pages.minecraft_server_address'):
            context['address'] = settings.MINECRAFT_SERVER_HOST
        if request.user.has_perm('pages.minecraft_server_players_count') and status.is_online:
            context['players'] = {}
            context['players']['online'] = status.player_count_online
            context['players']['max'] = status.player_count_max
    return context

def duty_context(request):
    "Gets information about who is on duty."
    context = {}
    shift = models.DutyShift.get_current_shift()
    if shift:
        context['name'] = shift.name
        if request.user.has_perm('pages.duty_phone') and shift.phone:
            context['phone'] = shift.phone
    else:
        context['info'] = "No RA on duty"
    return context

"""
Pages
"""
def home_page(request):
    "Displays the home page."
    context = base_context(request)
    context['duty'] = duty_context(request)
    context['minecraft'] = minecraft_context(request)
    context['page_title'] = "Home"
    return render(request, 'pages/home_page.html', context)

def events_page(request):
    "Displays the events page."
    context = base_context(request)
    return render(request, 'pages/events_page.html', context)
        
def tools_page(request):
    "Displays the tools page."
    context = base_context(request)
    context['duty'] = duty_context(request)
    context['minecraft_status'] = minecraft_context(request)
    if (request.user.has_perm('pages.minecraft_register')):
        context['minecraft_register'] = {}
        if (request.POST):
            new_registration = forms.MinecraftUserForm(request.POST).save(commit=False)
            new_registration.owner = request.user
            if not new_registration.is_valid():
                context['minecraft_register']['message'] = "Error! One or more fields were incorrect."
                context['minecraft_register']['form'] = forms.MinecraftUserForm()
            else:
                new_registration.save()
                request.user.permissions.remove('pages.minecraft_register')
                context['minecraft_register']['message'] = "You have successfully registered %s!" % new_registration.username
        else:
            context['minecraft_register']['form'] = forms.MinecraftUserForm()
    context['contact_form'] = {}
    context['contact_form']['form'] = forms.ContactForm()
    context['page_title'] = "Tools"
    return render(request, 'pages/tools_page.html', context)

def auth_page(request):
    "Minecraft authentication API."
    
    """	q=canJoin
	q=isRegistered
	q=isBanned
	q=authenticate"""
    if 'q' in request.GET and 'username' in request.GET:
        # look for the player with the given username
        user = models.MinecraftUser.objects.filter(username=request.GET['username'])
        if not user.exists():
            # nothing is true if the player doesn't exist
            return HttpResponse(False)
        user = user.first()
        # handle the query that was sent
        if request.GET['q'] == 'canJoin':
            result = not user.banned
        elif request.GET['q'] == 'isRegistered':
            result = True
        elif request.GET['q'] == 'isBanned':
            result = user.banned
        elif request.GET['q'] == 'canAuthenticate':
            if 'password' in request.GET:
                result = user.password == request.GET['password']
            else:
                result = False
        else:
            result = ""
        return HttpResponse(result)
    return tools_page(request)

