from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q

from .models import (
    Item, ItemImage, ContactForm, ReportPost,
    Feedback, Chat, Message
)
from .serializers import (
    UserSerializer, UserRegisterSerializer,
    ItemSerializer, ItemImageSerializer,
    ContactFormSerializer, ReportPostSerializer,
    FeedbackSerializer, ChatSerializer, MessageSerializer
)

User = get_user_model()

# =========================
# Permissions
# =========================
class IsOwnerOrReadOnly(permissions.BasePermission):
    """Only owners can edit/delete objects"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


# =========================
# User Views
# =========================
class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class DeleteAccountView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        request.user.delete()
        return Response(
            {"detail": "Account deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# =========================
# Item Views
# =========================
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.select_related("owner").prefetch_related("images")
    serializer_class = ItemSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save(owner=request.user)

        images = request.FILES.getlist("images")
        for image in images:
            ItemImage.objects.create(item=item, image=image)

        item.refresh_from_db()
        return Response(
            self.get_serializer(item).data,
            status=status.HTTP_201_CREATED
        )


# =========================
# Item Image Views
# =========================
class ItemImageViewSet(viewsets.ModelViewSet):
    serializer_class = ItemImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return ItemImage.objects.filter(item__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(item_id=self.request.data.get("item"))


# =========================
# Contact Form Views
# =========================
class ContactFormCreateView(generics.CreateAPIView):
    serializer_class = ContactFormSerializer
    permission_classes = [permissions.AllowAny]


class ContactFormListView(generics.ListAPIView):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
    permission_classes = [permissions.IsAdminUser]


# =========================
# Report Post Views
# =========================
class ReportPostCreateView(generics.CreateAPIView):
    serializer_class = ReportPostSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReportPostListView(generics.ListAPIView):
    queryset = ReportPost.objects.select_related("item", "user")
    serializer_class = ReportPostSerializer
    permission_classes = [permissions.IsAdminUser]


# =========================
# Feedback Views
# =========================
class FeedbackCreateView(generics.CreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]


class FeedbackListView(generics.ListAPIView):
    queryset = Feedback.objects.select_related("user")
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAdminUser]


# =========================
# Chat Views (FIXED)
# =========================
class ChatCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        item_id = request.data.get("item_id")
        item = get_object_or_404(Item, id=item_id)

        buyer = request.user
        seller = item.owner

        if buyer == seller:
            return Response(
                {"detail": "You cannot chat with yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        chat, _ = Chat.objects.get_or_create(
            item=item,
            buyer=buyer
        )

        return Response(
            ChatSerializer(chat).data,
            status=status.HTTP_200_OK
        )


class ChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(Q(buyer=user) | Q(item__owner=user)).distinct()


class ChatMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat = get_object_or_404(Chat, id=self.kwargs["chat_id"])

        if self.request.user not in [chat.buyer, chat.seller]:
            return Message.objects.none()

        return chat.messages.all()


class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        chat = get_object_or_404(
            Chat,
            id=self.request.data.get("chat")
        )

        if self.request.user not in [chat.buyer, chat.seller]:
            raise permissions.PermissionDenied()

        message = serializer.save(
            chat=chat,
            sender=self.request.user
        )

        chat.last_message_at = timezone.now()
        chat.save()

        return message
