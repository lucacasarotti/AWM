"""CineDate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from CineDate import settings
from main import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('main.urls'),namespace='main')),
    path('utenti/',include('utenti.urls')),
    path('inviti/', include('inviti.urls')),
    url('', include('social_django.urls', namespace='social')),
    path('chat/', include('chatroom.urls')),
    path('feedback/',include('feedback.urls', namespace='feedback')),
    path('api/',include('API.urls',namespace='API')),
    path('api/rest-auth/', include("rest_auth.urls")),
    path('api/rest-auth/registration/', include("rest_auth.registration.urls")),
    path('', include('contactus.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'main.views.error_404_view'
handler500 = 'main.views.error_500_view'
handler403 = 'main.views.error_403_view'
