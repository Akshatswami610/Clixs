from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    home,
    profile,
    login,
    signup,
    about,
    addpost,
    contactus,
    chat,
)

urlpatterns = [
    # =========================
    # Admin
    # =========================
    path('admin/', admin.site.urls),

    # =========================
    # API
    # =========================
    path('api/v1/', include('api.urls')),

    # =========================
    # Auth & User Pages
    # =========================
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),

    # =========================
    # Pages
    # =========================
    path('', home, name='home'),          # default landing page
    path('home/', home, name='home'),
    path('about/', about, name='about'),
    path('addpost/', addpost, name='addpost'),
    path('chat/', chat, name='chat'),
    path('contact/', contactus, name='contactus'),
]

# =========================
# Static & Media (DEV only)
# =========================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
