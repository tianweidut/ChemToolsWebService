# -*- coding: UTF-8 -*-
'''
Created on 2013-03-03

@author: tianwei

Desc: This module contains views that allow users to submit the calculated
      tasks.
'''
import datetime
import logging
import os
import sys

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden, Http404
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators import csrf
from django.contrib.auth.decorators import login_required

from backend.logging import logger
from users import models
from users import forms


@login_required
@csrf.csrf_protect
def profile(request):
    """
        Get or Post UserProfile
    """
    user = get_object_or_404(models.UserProfile,
                             user__username=request.user.username)
    if request.user != user.user and not request.user.is_superuser:
        raise Http404

    if request.method == "POST":
        form = forms.UserProfileForm(user, request.POST)
        if form.is_valid():
            user.workunit = form.cleaned_data["company"]
            user.telephone = form.cleaned_data["telephone"]
            user.address = form.cleaned_data["location"]
            user.machinecode = form.cleaned_data["machinecode"]
            user.save()

            HttpResponseRedirect("/settings/profile")
    else:
        form = forms.UserProfileForm(user)

    data = {"form": form}
    return render(request, "widgets/settings/profile.html", data)


@login_required
@csrf.csrf_protect
def admin_account(request):
    """
        Set Password
    """
    user = get_object_or_404(models.UserProfile,
                             user__username=request.user.username)
    if not (request.user == user.user or request.user.is_superuser):
        raise Http404

    if request.method == "POST":
        form = forms.PasswordForm(user, request.POST)
        if form.is_valid():
            user.user.set_password(form.cleaned_data["new_password"])
            user.user.save()
            HttpResponseRedirect("/info/")
    else:
        form = forms.PasswordForm(user)

    data = {"form": form}
    return render(request, "widgets/settings/admin.html", data)


@login_required
@csrf.csrf_protect
def billing(request):
    data = {}
    return render(request, "widgets/settings/billing.html", data)


@login_required
@csrf.csrf_protect
def payments(request):
    data = {}
    return render(request, "widgets/settings/payments.html", data)
