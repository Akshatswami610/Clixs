from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import (
    Item,
    ItemImage,
    ContactForm,
    ReportPost,
    Chat,
    Message,
)

User = get_user_model()

# ======================================================
# USER SERIALIZERS
# ======================================================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "phone_number",
            "registration_number",
            "first_name",
            "last_name",
        )


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "phone_number",
            "first_name",
            "last_name",
            "registration_number",
            "password",
            "confirm_password",
        )

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return User.objects.create_user(**validated_data)

# ======================================================
# ITEM SERIALIZERS
# ======================================================

class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ("id", "image", "uploaded_at")


class ItemSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    images = ItemImageSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = "__all__"
        read_only_fields = ("owner", "created_at")

# ======================================================
# CONTACT / REPORT / FEEDBACK
# ======================================================

class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = "__all__"
        read_only_fields = ("status", "created_at")


class ReportPostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = ReportPost
        fields = "__all__"
        read_only_fields = ("created_at",)


# =========================
# CHAT SERIALIZER (ANONYMOUS, PRODUCT-ONLY)
# =========================

class ChatSerializer(serializers.ModelSerializer):
    item_title = serializers.CharField(
        source="item_title_snapshot",
        read_only=True
    )
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = (
            "id",
            "item",
            "item_title",
            "created_at",
            "last_message_at",
            "last_message",
        )

    def get_last_message(self, obj):
        msg = obj.messages.last()
        return msg.text if msg else None


# =========================
# MESSAGE SERIALIZER (NO NAMES)
# =========================

class MessageSerializer(serializers.ModelSerializer):
    is_me = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            "chat",
            "text",
            "is_me",
            "created_at",
        )
        read_only_fields = ("id", "created_at", "is_me")

    def get_is_me(self, obj):
        request = self.context.get("request")
        return request and obj.sender == request.user

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["sender"] = request.user
        return super().create(validated_data)
