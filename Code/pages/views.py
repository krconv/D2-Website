from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.mail import mail_managers

import mcstatus
import requests
from dns.resolver import query
from django_ajax.decorators import ajax
from Daniels_Website.settings import common as settings
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
    return context

def minecraft_context(request):
    "Gets information about the server's address, status and player count."
    context = {}
    status = models.MinecraftServerPing.get_latest_status()
    if status:
        context['status'] = status.status
        context['is_online'] = status.is_online
        context['version'] = status.version
        context['date'] = status.date
        if request.user.has_perm('pages.minecraft_server_address'):
            context['address'] = settings.MINECRAFT_SERVER_HOST
        if request.user.has_perm('pages.minecraft_status_players_count') and status.is_online:
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
    context['posts'] = models.SitePost.objects.order_by('date')[:3]
    context['duty'] = duty_context(request)
    context['minecraft_status'] = minecraft_context(request)
    context['page_title'] = "Home"
    return render(request, 'pages/home_page.html', context)

def events_page(request):
    "Displays the events page."
    context = base_context(request)
    return render(request, 'pages/events_page.html', context)
        
def tools_page(request):
    "Displays the tools page."
    if (request.is_ajax()):
        return tools_page_post(request)
    context = base_context(request)
    context['duty'] = duty_context(request)
    context['minecraft_status'] = minecraft_context(request)
    # add the minecraft registration form if the user is allowed to see it
    if (request.user.has_perm('pages.minecraft_register')):
        # user is allowed to have a minecraft registration
        context['minecraft_form'] = {}
        context['minecraft_form']['form'] = forms.MinecraftUserForm()
        context['minecraft_form']['action'] = "update" 
        registered_accounts = models.MinecraftUser.objects.filter(owner=request.user)
        if registered_accounts.exists():
            context['minecraft_form']['form'] = forms.MinecraftUserForm(instance=registered_accounts.first())
            context['minecraft_form']['form'].fields['username'].widget.attrs['readonly'] = True
            context['minecraft_form']['action'] = "update" 
    # add the contact form
    context['contact_form'] = {}
    context['contact_form']['form'] = forms.ContactForm()
    context['recaptcha_site_key'] = settings.RECAPTCHA_SITE_KEY
    context['page_title'] = "Tools"
    return render(request, 'pages/tools_page.html', context)

@ajax
def tools_page_post(request):
    # handle any post requests
    if not request.POST or not 'g-recaptcha-response' in request.POST:
        # this is a bad state
        return { 'message' : "something went wrong..." , 'is_error' : True }

    # verify that the recaptcha is correct
    recaptcha_verify = requests.post(settings.RECAPTCHA_VERIFY_URL, data = {
        'secret' : settings.RECAPTCHA_SECRET_KEY,
        'response' : request.POST.get('g-recaptcha-response'),
        'remoteip' : request.META.get('REMOTE_ADDR'),
    }).json()
    if not recaptcha_verify['success']:
        # the recaptcha failed
        return { 'message' : "reCAPTCHA verification failed" , 'is_error' : True }

    is_error = False
    if 'minecraft_form' in request.POST:
        # user submitted a registration request
        form = forms.MinecraftUserForm(request.POST)
        matching_users = models.MinecraftUser.objects.filter(username=form['username'].value())
        if matching_users.exists() and matching_users.first().owner == request.user:
            # trying to modify an existing registration
            matching_users.first().password = form['password'].value()
            message = "password updated successfully"
        else:
            # trying to create a new registration
            owned_users = models.MinecraftUser.objects.filter(owner=request.user)
            if owned_users.exists():
                message = "you already have a minecraft registration!"
                is_error = True
            elif matching_users.exists():
                message = "that username has been taken!"
                is_error = True
            elif not form.is_valid():
                message = "the information provided is not valid!"
                is_error = True
            else:
                # successful registration
                registration = form.save(commit=False)
                registration.owner = request.user
                registration.save()
                message = "you have successfully registered %s!" % registration.username
    elif 'contact_form' in request.POST:
        # user submitted a contact form request
        contact_form = forms.ContactForm(request.POST)
        if not contact_form.is_valid():
            message = contact_form.errors.values()
            is_error = True
        else:
            mail_managers(
                "Contact Form Submission",
                "From: %s (%s, IP:%s)\r\n%s" % (
                    contact_form['name'].value(),
                    contact_form['email'].value(),
                    request.META.get('REMOTE_ADDR'),
                    contact_form['message'].value(),
                ),
                fail_silently=True
            )
            message = "your messsage was sent!"
    else:
        # someone is being naughty
        message = "something went wrong..."
        is_error = True

    return { 'message' : message, 'is_error' : is_error }

def auth_page(request):
    """
    Minecraft authentication API
    """
    # make sure that the request is coming from the minecraft server
    is_from_minecraft_server = False
    try:
        server_ip = str(query(settings.MINECRAFT_SERVER_HOST)[0])
        is_from_minecraft_server = request.META.get('REMOTE_ADDR') == server_ip
    except Exception as e:
        pass
    if is_from_minecraft_server and 'q' in request.GET and 'username' in request.GET:
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
