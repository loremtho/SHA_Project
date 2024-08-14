# imagegen/urls.py
from django.urls import path
from .views import image_generate_view

urlpatterns = [
    path('', image_generate_view, name='generate'),
]
