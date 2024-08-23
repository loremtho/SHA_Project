from django.urls import path
from . import views
from . import auth_views  # 새로 생성된 auth_views 파일을 가져옴

urlpatterns = [
    path('', views.image_generate_view, name='generate'),
    path('login/', auth_views.login_view, name='login'),
    path('signup/', auth_views.signup_view, name='signup'),
    path('logout/', auth_views.logout_view, name='logout'),
]
