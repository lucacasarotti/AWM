from django.shortcuts import render
from .models import Invito


def home(request):
    context = {
        'inviti': Invito.objects.all()
    }
    return render(request, 'inviti/home.html', context)


def about(request):
    return render(request, 'inviti/about.html', {'title': 'About'})