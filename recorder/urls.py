from django.urls import path
from . import views

urlpatterns = [
    path('', views.recorder, name='recorder'),
    path('settings/', views.settings, name='settings'),
    path('api/settings/', views.get_settings, name='get_settings'),
]
