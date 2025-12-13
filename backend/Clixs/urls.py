from django.contrib import admin
from django.urls import path, include
from .views import home, profile, login, signup, browse, post, contactus, chat
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/v1/', include('api.urls')),
    path('login', login, name='login'),
    path('signup', signup, name='signup'),
    path('', home, name='home'),
    path('home', home, name='home'),
    path('browse', browse, name='browse'),
    path('post', post, name='post'),
    path('chat', chat, name='chat'),
    path('profile', profile, name='profile'),
    path('contactus', contactus, name='contactus'),
]


# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)