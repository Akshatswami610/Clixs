from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import (
    CustomUser,
    Item,
    ItemImage,
    ContactForm,
    ReportPost,
    Chat,
    Message,
)

# =========================
# Custom User Forms
# =========================
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "phone_number",
            "first_name",
            "last_name",
            "registration_number",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "__all__"


# =========================
# Custom User Admin
# =========================
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = (
        "phone_number",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "date_joined",
    )

    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = (
        "phone_number",
        "first_name",
        "last_name",
        "registration_number",
    )
    ordering = ("-date_joined",)

    readonly_fields = ("last_login", "date_joined")

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "registration_number")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "registration_number",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


# =========================
# Item Admin
# =========================
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("title", "item_type", "status", "owner", "created_at")
    list_filter = ("item_type", "status", "category")
    search_fields = ("title", "description", "category")
    autocomplete_fields = ("owner",)
    readonly_fields = ("created_at",)


# =========================
# Item Image Admin
# =========================
@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    list_display = ("item", "uploaded_at")
    autocomplete_fields = ("item",)
    readonly_fields = ("uploaded_at",)


# =========================
# Contact Form Admin
# =========================
@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "email", "phone", "subject")
    readonly_fields = ("created_at",)


# =========================
# Report Post Admin
# =========================
@admin.register(ReportPost)
class ReportPostAdmin(admin.ModelAdmin):
    list_display = ("item", "user", "created_at")
    autocomplete_fields = ("item", "user")
    readonly_fields = ("created_at",)


# =========================
# Chat Admin (UPDATED)
# =========================
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "item",
        "buyer",
        "seller",
        "created_at",
        "last_message_at",
    )
    search_fields = (
        "item__title",
        "buyer__phone_number",
        "item__owner__phone_number",
    )
    autocomplete_fields = ("item", "buyer")
    readonly_fields = ("created_at", "last_message_at")

    def seller(self, obj):
        return obj.item.owner

    seller.short_description = "Seller"


# =========================
# Message Admin (UPDATED)
# =========================
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "chat",
        "sender",
        "short_text",
        "created_at",
        "read_status",
    )
    list_filter = ("created_at",)
    search_fields = (
        "text",
        "sender__phone_number",
        "chat__item__title",
    )
    autocomplete_fields = ("chat", "sender")
    readonly_fields = ("created_at",)

    def short_text(self, obj):
        return obj.text[:40]

    short_text.short_description = "Message"

    def read_status(self, obj):
        return "Read" if obj.read_at else "Unread"

    read_status.short_description = "Status"
