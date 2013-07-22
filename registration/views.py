# -*- coding: UTF-8 -*-
'''
Created on 2012-11-10

@author: tianwei
'''

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from registration.forms import RegistrationFormUniqueEmail
from registration.models import RegistrationProfile


def active(request, activation_key,
           template_name='registration/activate.html',
           extra_context=None):
    """
    Active the user account from an activation key.
    """
    activation_key = activation_key.lower()
    account = RegistrationProfile.objects.activate_user(activation_key)
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              {'account': account,
                               'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS
                               },
                              context_instance=context)


def register(request, success_url=None,
             form_class=RegistrationFormUniqueEmail, profile_callback=None,
             template_name='registration/registration_form.html',
             extra_context=None):
    """
     Allow a new user to register an account.
    """
    if request.method == "POST":
        form = form_class(data=request.POST)
        if form.is_valid():
            new_user = form.save(request, profile_callback=profile_callback)
            #TODO: add userprofile
            # success_url needs to be dynamically generated here; setting a
            # a default value using reverse() will cause circular-import
            # problems with the default URLConf for this application, which
            # imports this file.
            return HttpResponseRedirect(success_url or reverse('registration_complete'))
    else:
        form = form_class()

    if extra_context is None:
        extra_context = {}

    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              {'form': form},
                              context_instance=context)
