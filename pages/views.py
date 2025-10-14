from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.utils.translation import gettext as _
from django.contrib import messages

from pages.forms import ContactForm

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutUsPageView(TemplateView):
    template_name = 'pages/aboutus.html'

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)

            if request.user.is_authenticated:
                contact.user = request.user
                contact.full_name = f"{request.user.first_name} {request.user.last_name}"
                contact.email = request.user.email

            contact.save()
            messages.success(request,_("your message was sent successfully"))
            return redirect('pages:home') 
        else:
            messages.error(request, _("please fill the fields correctlly"))
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})
