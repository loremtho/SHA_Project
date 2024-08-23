from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns = [
    # 기존 URL 패턴들
    path('admin/', admin.site.urls),
    path('', include('imagegen.urls')),  # imagegen 앱의 URL을 포함
    path('board/', include('board.urls')),  # 게시판 앱의 URL 포함
    path('accounts/', include('django.contrib.auth.urls')),  # Django 기본 인증 URL 포함
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)