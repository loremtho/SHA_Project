from django.urls import path
from .views import image_generate_view, login_view, signup_view

urlpatterns = [
    path('', image_generate_view, name='generate'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
]
