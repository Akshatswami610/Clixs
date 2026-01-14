from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
from django.core.exceptions import ValidationError


# =========================
# Custom User Manager
# =========================
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(phone_number, password, **extra_fields)


# =========================
# Custom User Model
# =========================
class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    registration_number = models.PositiveIntegerField(unique=True, null=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.phone_number


# =========================
# Item (Product)
# =========================
class Item(models.Model):
    ITEM_TYPES = (
        ("SELL", "Sell"),
        ("RENT", "Rent"),
    )

    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("SOLD", "Sold"),
        ("RENTED", "Rented"),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()

    item_type = models.CharField(max_length=5, choices=ITEM_TYPES)

    sell_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    rent_prices = models.JSONField(
        null=True,
        blank=True,
        help_text="Example: {'daily': 100, 'weekly': 500}"
    )

    category = models.CharField(max_length=50, blank=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="items"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.item_type == "SELL" and not self.sell_price:
            raise ValidationError("Sell price required for SELL items")

        if self.item_type == "RENT" and not isinstance(self.rent_prices, dict):
            raise ValidationError("Rent prices required for RENT items")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# =========================
# Item Images
# =========================
class ItemImage(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="clixs/items/")
    uploaded_at = models.DateTimeField(auto_now_add=True)


# =========================
# Chat (Product-based, Anonymous UI)
# =========================
class Chat(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="chats"
    )

    # Snapshot for fast UI + historical safety
    item_title_snapshot = models.CharField(max_length=100, editable=False)

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="buyer_chats"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("item", "buyer")
        ordering = ["-last_message_at"]
        indexes = [
            models.Index(fields=["buyer"]),
            models.Index(fields=["item"]),
        ]

    @property
    def seller(self):
        return self.item.owner

    def clean(self):
        if self.buyer == self.item.owner:
            raise ValidationError("Cannot chat with yourself")

        if self.item.status != "ACTIVE":
            raise ValidationError("Chat not allowed on inactive items")

    def save(self, *args, **kwargs):
        if not self.item_title_snapshot:
            self.item_title_snapshot = self.item.title

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Chat: {self.item_title_snapshot}"


# =========================
# Message (No Names Exposed)
# =========================
class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    text = models.TextField(max_length=2000)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["chat"]),
            models.Index(fields=["created_at"]),
        ]

    def clean(self):
        if self.sender not in [self.chat.buyer, self.chat.seller]:
            raise ValidationError("Sender not part of this chat")

        if self.chat.item.status != "ACTIVE":
            raise ValidationError("Messaging closed for this item")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        Chat.objects.filter(id=self.chat_id).update(
            last_message_at=self.created_at
        )

    def __str__(self):
        return f"Message in {self.chat.id}"


# =========================
# Report Item
# =========================
class ReportPost(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)


# =========================
# Feedback
# =========================
class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
