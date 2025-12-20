from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # =========================
    # Django Admin
    # =========================
    path("admin/", admin.site.urls),

    # =========================
    # API v1 (Core Backend)
    # =========================
    path("api/v1/", include("api.urls")),

    # =========================
    # JWT Authentication (React uses these)
    # =========================
    path("api/v1/auth/login/", TokenObtainPairView.as_view(), name="jwt-login"),
    path("api/v1/auth/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
]

# =========================
# Static & Media (DEV only)
# =========================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
