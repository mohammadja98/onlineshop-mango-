from django.urls import path
from .views import HomePageView,AboutUsPageView, ContactPageView

app_name='pages'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('aboutus/', AboutUsPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact')
]
