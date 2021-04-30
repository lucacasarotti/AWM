from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.conf import settings


@login_required(login_url='/utenti/login/')
def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['oggetto']
            message = form.cleaned_data['messaggio']
            try:
                send_mail(subject, message, request.user.email, [settings.EMAIL_HOST_USER])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, "contactus/email_form.html", {'success': True})
    return render(request, "contactus/email_form.html", {'form': form, 'success': False})
