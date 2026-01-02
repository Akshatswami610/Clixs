from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    UserRegisterView,
    UserProfileView,
    ItemViewSet,
    ItemImageViewSet,
    ContactFormCreateView,
    ContactFormListView,
    ReportPostCreateView,
    ReportPostListView,
    FeedbackCreateView,
    FeedbackListView,
    DeleteAccountView
)

router = DefaultRouter()
router.register(r"items", ItemViewSet, basename="item")
router.register(r"item-images", ItemImageViewSet, basename="item-image")

urlpatterns = [
    # =========================
    # AUTH (JWT)
    # =========================
    path("auth/register/", UserRegisterView.as_view(), name="user-register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/profile/", UserProfileView.as_view(), name="user-profile"),
    path("auth/delete-account/", DeleteAccountView.as_view(), name="delete-account"),

    # =========================
    # ITEMS
    # =========================
    path("", include(router.urls)),

    # =========================
    # CONTACT
    # =========================
    path("contact/", ContactFormCreateView.as_view(), name="contact-create"),
    path("contact/list/", ContactFormListView.as_view(), name="contact-list"),

    # =========================
    # REPORTS
    # =========================
    path("reports/", ReportPostCreateView.as_view(), name="report-create"),
    path("reports/list/", ReportPostListView.as_view(), name="report-list"),

    # =========================
    # FEEDBACK
    # =========================
    path("feedback/", FeedbackCreateView.as_view(), name="feedback-create"),
    path("feedback/list/", FeedbackListView.as_view(), name="feedback-list"),
]
