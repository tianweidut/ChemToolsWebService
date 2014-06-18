# coding: utf-8
import datetime
import random
import re
from hashlib import sha1
import uuid

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.db import models
from django.core.mail import send_mail

from utils import loginfo

DEFAULT_CREATE_ID = "0000-0000"
DEFAULT_ERROR_ID = "FFFF-FFFF"
SHA1_RE = re.compile('^[a-f0-9]{40}$')  # Activation Key


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    agentID = models.CharField(max_length=40,
                               default=lambda: str(uuid.uuid4()),
                               unique=True)
    workunit = models.CharField(max_length=2000, blank=True)
    address = models.CharField(max_length=2000, blank=True)
    telephone = models.CharField(max_length=100, blank=True)

    class meta:
        verbose_name = u"用户信息"
        verbose_name_plural = u"用户信息"

    def __unicode__(self):
        return '%s' % (self.user)


class RegistrationManager(models.Manager):
    """
    Custom manager for ``RegistrationProfile`` model.
    The methods defined here provide shortcuts for account creation
    and activation (including generation and emailing of activation
    keys), and for cleaning out expired inactive accounts.    
    """
    def activate_user(self, activation_key):
        """
        Validate an activation key and activation the corresponding User if vaild.
        """
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not profile.activation_key_expired():
                user = profile.user
                user.is_active = True
                user.save()
                profile.activation_key = "ALREADY_ACTIVATED"
                profile.save()
                return user

        return False

    def create_inactive_user(self, request,
                             username, password, email,
                             send_email=True, profile_callback=None):
        """
        Create a new, inactive ``User``, generates a
        ``RegistrationProfile`` and email its activation key to the
        ``User``, returning the new ``User``.
        """
        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.save()

        try:
            new_profile = UserProfile.objects.create(user=new_user)
            new_profile.save()
        except Exception, err:
            #TODO: later, we should process the object is empty, as the same
            #word, the adminuser should import base data into database, maybe
            #a log record for admin user is necessary
            loginfo(p=err)

        registration_profile = self.create_profile(new_user)

        if profile_callback is not None:
            profile_callback(user=new_user)

        if send_email:
            subject = render_to_string('registration/activation_email_subject.txt',
                                       {'site': get_current_site(request)})

            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            message = render_to_string('registration/activation_email.txt',
                                       {'activation_key': registration_profile.activation_key,
                                        'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                                        'site': get_current_site(request)})
            send_mail(subject,
                      message,
                      settings.DEFAULT_FROM_EMAIL,
                      [new_user.email])
        return new_user

    def create_profile(self,user):
        """
        Create a ``RegistrationProfile`` for a given
        ``User``, and return the ``RegistrationProfile``.
        """
        salt = sha1(str(random.random())).hexdigest()[:5]
        activation_key = sha1(salt+user.username).hexdigest()

        return self.create(user=user,
                           activation_key=activation_key)

    def delete_expired_users(self):
        """
        Remove expired instances of ``RegistrationProfile`` and their associated ``User``s.
        It is recommended that this method be executed regularly as
        part of your routine site maintenance; this application
        provides a custom management command which will call this
        method, accessible as ``manage.py cleanupregistration``.
        """
        for profile in self.all():
            if profile.activation_key_expired():
                user = profile.user
                if not user.is_active:
                    user.delete()


class RegistrationProfile(models.Model):
    """
    A simple profile which stores an activation key for use during user account registration
    """
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    activation_key = models.CharField(_('activation key'), max_length=40)

    objects = RegistrationManager()

    class Meta:
        verbose_name = u'注册信息'
        verbose_name_plural = u'注册信息'

    def __unicode__(self):
        return u"Registration information for %s" % self.user

    def activation_key_expired(self):
        """
        Determine whether this ``RegistrationProfile``'s activation
        key has expired, returning a boolean -- ``True`` if the key
        has expired.
        """
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == "ALREADY_ACTIVATED" or \
               (self.user.date_joined + expiration_date <= datetime.datetime.now())

    activation_key_expired.boolean = True
