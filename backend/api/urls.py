from django.urls import path, include
from rest_framework.routers import DefaultRouter

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
)

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')
router.register(r'item-images', ItemImageViewSet, basename='item-image')

urlpatterns = [
    # =========================
    # User URLs
    # =========================
    path('auth/register/', UserRegisterView.as_view(), name='user-register'),
    path('auth/profile/', UserProfileView.as_view(), name='user-profile'),

    # =========================
    # Router URLs (Items & Images)
    # =========================
    path('', include(router.urls)),

    # =========================
    # Contact Form
    # =========================
    path('contact/', ContactFormCreateView.as_view(), name='contact-create'),
    path('admin/contact/', ContactFormListView.as_view(), name='contact-list'),

    # =========================
    # Report Posts
    # =========================
    path('reports/', ReportPostCreateView.as_view(), name='report-create'),
    path('admin/reports/', ReportPostListView.as_view(), name='report-list'),

    # =========================
    # Feedback
    # =========================
    path('feedback/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('admin/feedback/', FeedbackListView.as_view(), name='feedback-list'),
]
