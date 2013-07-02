# -*- coding: UTF-8 -*-
'''
Created on 2013-06-16

@author: tianwei
'''

from django.contrib.auth.models import User
from django.conf.urls.defaults import *
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ALL, ALL_WITH_RELATIONS


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        fields = ["username", "email", "first_name", "date_joined"]
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        filtering = {'username': ALL}


    def prepend_urls(self):
        return [url(r"^(?P<resource_name>%s)/(?P<username>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'),\
                name="api_dispatch_detail"),]

    def dehydrate(self, bundle):
        bundle.data['custom_field'] = "Hello world"
        return bundle

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)

    def get_object_list(self, request, *args, **kwargs):
        return User.objects.filter(username=request.user.username)
