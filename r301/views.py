import datetime
import json
import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from django.middleware import csrf
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .models import *


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        context = {
            'username': request.user.username
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        long_url = request.POST['long_url']
        short_url = request.POST['short_url']
        try:
            URLMap.objects.create(long_url=long_url, short_url=short_url)
        except:
            messages.error(request, f"That short URL r301.cf/{request.POST['short_url']} is already in use. Try something else.")
        else:
            messages.success(request, f"Short URL http://r301.cf/{request.POST['short_url']} has been created successfully.")
        return redirect('/')


class UrlView(View):

    def get(self, request, short_url):
        # if the user requests admin page, take them to login page
        if short_url[:5] == 'admin':
            return redirect('/admin/login')
        
        urlmap = URLMap.objects.filter(short_url=short_url).first()
        if urlmap is None:
            return HttpResponse('404: could not find destination for redirect.', status=404)
        return redirect(urlmap.long_url)
