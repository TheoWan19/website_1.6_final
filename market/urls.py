from django.urls import path

from . import views

urlpatterns = [
    path('live', views.live, name='live'),
    path('team/<int:pk>', views.team_details, name='team'),
]