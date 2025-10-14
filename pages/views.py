from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from pages.forms import ContactForm

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutUsPageView(TemplateView):
    template_name = 'pages/aboutus.html'

# class ContactPageView(TemplateView):
#     template_name = 'pages/contact.html'

from django.shortcuts import render, redirect
from .forms import ContactForm

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)

            if request.user.is_authenticated:
                # اگر لاگین بود، اطلاعاتش جایگزین میشه
                contact.user = request.user
                contact.full_name = f"{request.user.first_name} {request.user.last_name}"
                contact.email = request.user.email

            contact.save()
            return redirect('pages:home')  # یا هر صفحه دیگه مثل success_page
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})
