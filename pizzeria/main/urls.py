from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('about', views.about, name='about'),
    path('account', views.account, name='account')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)