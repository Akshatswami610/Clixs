from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    # User
    UserRegisterView,
    UserProfileView,
    DeleteAccountView,

    # Items
    ItemViewSet,
    ItemImageViewSet,

    # Contact / Report / Feedback
    ContactFormCreateView,
    ContactFormListView,
    ReportPostCreateView,
    ReportPostListView,
    FeedbackCreateView,
    FeedbackListView,

    # Chat
    ChatCreateView,
    ChatListView,
    ChatMessagesView,
    SendMessageView,
)

# =========================
# Routers
# =========================
router = DefaultRouter()
router.register(r"items", ItemViewSet, basename="item")
router.register(r"item-images", ItemImageViewSet, basename="item-image")

# =========================
# URL Patterns
# =========================
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
    # CHAT
    # =========================
    path("chats/", ChatListView.as_view(), name="chat-list"),
    path("chats/create/", ChatCreateView.as_view(), name="chat-create"),
    path(
        "chats/<int:chat_id>/messages/",
        ChatMessagesView.as_view(),
        name="chat-messages",
    ),
    path(
        "messages/send/",
        SendMessageView.as_view(),
        name="send-message",
    ),
]
