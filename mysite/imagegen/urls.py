from django.urls import path
from .views import image_generate_view, login_view, signup_view, logout_view, generate_image_view

urlpatterns = [
    path('', image_generate_view, name='generate'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('generate-image/', generate_image_view, name='generate_image'),  # 추가된 경로
]
