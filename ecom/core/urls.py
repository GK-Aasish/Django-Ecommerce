from django.urls import path
from .views.main_views import home

urlpatterns = [
    path('', home, name='home')
]