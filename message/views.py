from django.contrib import messages
from django.shortcuts import render, redirect

from message.forms import MessageForm
from message.models import Contact


# Create your views here.

def contact(request):
    context = {
        'active_page': 'contacts'
    }
    return render(request, 'store/contact.html', context)


def send_message(request):
    current_user = request.user
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            data = Contact()
            if request.user.is_authenticated:
                contact.user = request.user
            else:
                contact.user = None
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.message = form.cleaned_data['message']
            data.save()
            messages.success(request,"Thank you! We will contact you soon.")
            return redirect(url)

