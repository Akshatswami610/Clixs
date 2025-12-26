from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import (
    Item,
    ItemImage,
    ContactForm,
    ReportPost,
    Feedback,
)

User = get_user_model()


# =========================
# User Serializers
# =========================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "phone_number",
            "registration_number",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
        )
        read_only_fields = ("id", "is_active", "date_joined")


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = (
            "phone_number",
            "first_name",
            "last_name",
            "password",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user


# =========================
# Item Image Serializer
# =========================

class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = (
            "id",
            "image",
            "uploaded_at",
        )
        read_only_fields = ("id", "uploaded_at")


# =========================
# Item Serializers
# =========================

class ItemSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    images = ItemImageSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = (
            "id",
            "title",
            "description",
            "item_type",
            "sell_price",
            "rent_prices",
            "category",
            "status",
            "owner",
            "images",
            "created_at",
        )
        read_only_fields = (
            "id",
            "owner",
            "created_at",
        )

    def validate(self, attrs):
        item_type = attrs.get("item_type")
        sell_price = attrs.get("sell_price")
        rent_prices = attrs.get("rent_prices")

        if item_type == "SELL":
            if not sell_price:
                raise serializers.ValidationError(
                    {"sell_price": "Sell price is required for SELL items."}
                )
            if rent_prices:
                raise serializers.ValidationError(
                    {"rent_prices": "Rent prices are not allowed for SELL items."}
                )

        if item_type == "RENT":
            if not rent_prices:
                raise serializers.ValidationError(
                    {"rent_prices": "Rent pricing is required for RENT items."}
                )
            if not isinstance(rent_prices, dict):
                raise serializers.ValidationError(
                    {"rent_prices": "Rent prices must be a dictionary."}
                )
            for key, value in rent_prices.items():
                if not isinstance(value, (int, float)):
                    raise serializers.ValidationError(
                        {"rent_prices": f"Invalid price for {key}."}
                    )

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["owner"] = request.user
        return super().create(validated_data)


# =========================
# Contact Form Serializer
# =========================

class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = (
            "id",
            "name",
            "email",
            "phone",
            "subject",
            "message",
            "status",
            "created_at",
        )
        read_only_fields = (
            "id",
            "status",
            "created_at",
        )

    def validate(self, attrs):
        if not attrs.get("email") and not attrs.get("phone"):
            raise serializers.ValidationError(
                "Provide either email or phone."
            )
        return attrs


# =========================
# Report Post Serializer
# =========================

class ReportPostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = ReportPost
        fields = (
            "id",
            "item",
            "user",
            "reason",
            "created_at",
        )
        read_only_fields = ("id", "created_at")


# =========================
# Feedback Serializer
# =========================

class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Feedback
        fields = (
            "id",
            "user",
            "feedback",
            "created_at",
        )
        read_only_fields = ("id", "created_at")
