from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import (
    CustomUser,
    Item,
    ItemImage,
    ContactForm,
    ReportPost,
)

# =========================
# Custom User Forms
# =========================
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("phone_number", "first_name", "last_name", "email")


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

    search_fields = ("phone_number", "first_name", "last_name", "email")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email")}),
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
                    "email",
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
    list_display = ("title", "item_type", "status", "created_at")
    list_filter = ("item_type", "status", "category")
    search_fields = ("title", "description", "category")
    autocomplete_fields = ("owner",)


# =========================
# Item Image Admin
# =========================
@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    list_display = ("item", "uploaded_at")
    autocomplete_fields = ("item",)


# =========================
# Contact Form Admin
# =========================
@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "created_at")
    search_fields = ("name", "email", "phone", "subject")
    readonly_fields = ("created_at",)


# =========================
# Report Post Admin
# =========================
@admin.register(ReportPost)
class ReportPostAdmin(admin.ModelAdmin):
    list_display = ("item", "user", "created_at")
    autocomplete_fields = ("item", "user")
