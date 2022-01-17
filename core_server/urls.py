# -*- coding:utf-8 -*-
'''
__author__ = 'XD'
__mtime__ = 2022/1/17
__project__ = weibo_commnet_server
Fix the Problem, Not the Blame.
'''

from django.urls import include, path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="core_server/index.html")),
    path("comment", views.get_comments)
]
