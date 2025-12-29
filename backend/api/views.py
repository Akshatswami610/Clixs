from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model

from .models import (
    Item,
    ItemImage,
    ContactForm,
    ReportPost,
    Feedback,
)
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    ItemSerializer,
    ItemImageSerializer,
    ContactFormSerializer,
    ReportPostSerializer,
    FeedbackSerializer,
)

User = get_user_model()


# =========================
# Permissions
# =========================

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only owners can edit/delete objects
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


# =========================
# User Views
# =========================

class UserRegisterView(generics.CreateAPIView):
    """
    User Registration
    """
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(generics.RetrieveAPIView):
    """
    Get logged-in user profile
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# =========================
# Item Views
# =========================

class ItemViewSet(viewsets.ModelViewSet):
    """
    CRUD for Items
    """
    queryset = Item.objects.select_related("owner").prefetch_related("images").all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]  # Added to handle file uploads

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Override create to handle image uploads
        """
        # Serialize and validate item data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the item
        item = serializer.save(owner=request.user)

        # Handle image uploads - get all images from request.FILES
        images = request.FILES.getlist('images')

        # Create ItemImage objects for each uploaded image
        for image_file in images:
            ItemImage.objects.create(item=item, image=image_file)

        # Refresh the item to include the newly created images
        item.refresh_from_db()

        # Return the complete item data with images
        output_serializer = self.get_serializer(item)
        headers = self.get_success_headers(output_serializer.data)

        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


# =========================
# Item Image Views
# =========================

class ItemImageViewSet(viewsets.ModelViewSet):
    """
    Upload & delete item images
    """
    serializer_class = ItemImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return ItemImage.objects.filter(item__owner=self.request.user)

    def perform_create(self, serializer):
        item_id = self.request.data.get("item")
        serializer.save(item_id=item_id)


# =========================
# Contact Form Views
# =========================

class ContactFormCreateView(generics.CreateAPIView):
    """
    Public contact form submission
    """
    serializer_class = ContactFormSerializer
    permission_classes = [permissions.AllowAny]


class ContactFormListView(generics.ListAPIView):
    """
    Admin view for contact messages
    """
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
    permission_classes = [permissions.IsAdminUser]


# =========================
# Report Post Views
# =========================

class ReportPostCreateView(generics.CreateAPIView):
    """
    Report an item
    """
    serializer_class = ReportPostSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReportPostListView(generics.ListAPIView):
    """
    Admin view for reported posts
    """
    queryset = ReportPost.objects.select_related("item", "user")
    serializer_class = ReportPostSerializer
    permission_classes = [permissions.IsAdminUser]


# =========================
# Feedback Views
# =========================

class FeedbackCreateView(generics.CreateAPIView):
    """
    Submit feedback
    """
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]


class FeedbackListView(generics.ListAPIView):
    """
    Admin view for feedback
    """
    queryset = Feedback.objects.select_related("user")
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAdminUser]