from django.urls import path
from .views import HomePageView,AboutUsPageView, contact_view

app_name='pages'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('aboutus/', AboutUsPageView.as_view(), name='about'),
    path('contact/', contact_view, name='contact')
]
