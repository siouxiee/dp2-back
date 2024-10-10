from django.http import HttpResponse
from django.shortcuts import redirect
from allauth.socialaccount.models import SocialAccount

def index(request):
    return HttpResponse("Backend en Django: Helados Villaizan")

def facebook_login(request):
    # Redirige al login de Facebook
    return redirect('/accounts/facebook/login/')

def instagram_login(request):
    # Redirige al login de Instagram
    return redirect('/accounts/instagram/login/')
