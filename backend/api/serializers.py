from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import (
    Item,
    ItemImage,
    ContactForm,
    ReportPost,
    Feedback,
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


class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Feedback
        fields = "__all__"
        read_only_fields = ("created_at",)

# ======================================================
# CHAT SERIALIZER (FIXED)
# ======================================================

class ChatSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    seller = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = (
            "id",
            "item",
            "buyer",
            "seller",
            "other_user",
            "last_message",
            "created_at",
            "last_message_at",
        )
        read_only_fields = (
            "buyer",
            "seller",
            "created_at",
            "last_message_at",
        )

    def get_other_user(self, obj):
        request = self.context.get("request")

        if request and request.user == obj.buyer:
            user = obj.item.owner
        else:
            user = obj.buyer

        return {
            "id": user.id,
            "phone_number": user.phone_number,
            "name": f"{user.first_name} {user.last_name}".strip()
        }

    def get_seller(self, obj):
        user = obj.item.owner
        return {
            "id": user.id,
            "phone_number": user.phone_number,
            "name": f"{user.first_name} {user.last_name}".strip()
        }

    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        return last_msg.text if last_msg else None

# ======================================================
# MESSAGE SERIALIZER (FIXED)
# ======================================================

class MessageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source="text", read_only=True)
    sender_id = serializers.IntegerField(source="sender.id", read_only=True)
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            "chat",
            "sender_id",
            "content",
            "text",
            "is_read",
            "created_at",
        )
        read_only_fields = (
            "id",
            "sender_id",
            "created_at",
            "content",
            "is_read",
        )

    def get_is_read(self, obj):
        return bool(obj.read_at)

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["sender"] = request.user
        return super().create(validated_data)
