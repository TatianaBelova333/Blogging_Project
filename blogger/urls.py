from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('', include('users.urls', namespace='users')),
    path('', include('posts.urls', namespace='posts')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

