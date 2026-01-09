from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # =========================
    # Admin
    # =========================
    path("admin/", admin.site.urls),

    # =========================
    # API
    # =========================
    path("api/v1/", include("api.urls")),

    # =========================
    # Auth Pages
    # =========================
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("profile/", views.profile, name="profile"),

    # =========================
    # Pages
    # =========================
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("item-detail/", views.itemdetail, name="item-detail"),
    path("about/", views.about, name="about"),
    path("addpost/", views.addpost, name="addpost"),
    path("chats/", views.chats, name="chats"),
    path("contact/", views.contactus, name="contactus"),
    path("terms/", views.terms, name="terms"),
    path("privacy/", views.privacy, name="privacy"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
