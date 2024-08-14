from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 기존 URL 패턴들
    path('admin/', admin.site.urls),
    path('', include('imagegen.urls')),  # imagegen 앱의 URL을 포함
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)