from unicodedata import name
from django.urls import path
from . import views


urlpatterns = [
    path('fpl/', views.fpl, name='fpl'),
    path('fpl-admin', views.fpl_admin, name='fpl-admin')
]