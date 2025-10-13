from django.shortcuts import render
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutUsPageView(TemplateView):
    template_name = 'pages/aboutus.html'

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'