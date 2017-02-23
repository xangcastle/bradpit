from django.shortcuts import render
from django.views.generic.base import TemplateView


class Index(TemplateView):
    template_name = "app/base.html"





