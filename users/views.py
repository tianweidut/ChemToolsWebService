# coding: utf-8

from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators import csrf
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from users.models import RegistrationProfile, UserProfile
from users.forms import (RegistrationFormUniqueEmail, UserProfileForm,
                         PasswordForm)
from utils import basic_auth_api, make_json_response


@require_POST
@csrf_exempt
def api_login(request):
    if not basic_auth_api(request):
        return HttpResponseForbidden()

    if request.user.username:
        info = "login succeed"
        status = True
    else:
        info = "login failed"
        status = False

    return make_json_response(dict(info=info, status=status))


@login_required
@csrf.csrf_protect
def profile(request):
    user = get_object_or_404(UserProfile,
                             user__username=request.user.username)
    if request.user != user.user and not request.user.is_superuser:
        raise Http404

    if request.method == "POST":
        form = UserProfileForm(user, request.POST)
        if form.is_valid():
            user.workunit = form.cleaned_data["company"]
            user.telephone = form.cleaned_data["telephone"]
            user.address = form.cleaned_data["location"]
            user.save()

            HttpResponseRedirect("/settings/profile")
    else:
        form = UserProfileForm(user)

    data = {"form": form}
    return render(request, "widgets/settings/profile.html", data)


@login_required
@csrf.csrf_protect
def admin_account(request):
    user = get_object_or_404(UserProfile,
                             user__username=request.user.username)
    if not (request.user == user.user or request.user.is_superuser):
        raise Http404

    if request.method == "POST":
        form = PasswordForm(user, request.POST)
        if form.is_valid():
            user.user.set_password(form.cleaned_data["new_password"])
            user.user.save()
            HttpResponseRedirect("/info/")
    else:
        form = PasswordForm(user)

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


def active(request, activation_key,
           template_name='registration/activate.html',
           extra_context=None):
    activation_key = activation_key.lower()
    account = RegistrationProfile.objects.activate_user(activation_key)
    if extra_context is None:
        extra_context = {}

    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    data = {'account': account,
            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS}

    return render_to_response(template_name, data,
                              context_instance=context)


def register(request, success_url=None,
             form_class=RegistrationFormUniqueEmail, profile_callback=None,
             template_name='registration/register.html',
             extra_context=None):
    if request.method == "POST":
        form = form_class(data=request.POST)
        if form.is_valid():
            form.save(request, profile_callback=profile_callback)
            return HttpResponseRedirect(
                success_url or reverse('registration_complete'))
    else:
        form = form_class()

    if extra_context is None:
        extra_context = {}

    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    data = {'form': form}
    return render_to_response(template_name, data,
                              context_instance=context)
