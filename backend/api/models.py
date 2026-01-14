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
            raise ValueError("The phone number must be set")

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
# Item Model
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
        help_text="Example: {'daily': 50, 'weekly': 300}"
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
        if self.item_type == "SELL":
            if not self.sell_price:
                raise ValidationError("Sell price is required.")
            if self.rent_prices:
                raise ValidationError("Rent prices not allowed for SELL items.")

        if self.item_type == "RENT":
            if not isinstance(self.rent_prices, dict):
                raise ValidationError("Rent prices must be a dictionary.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# =========================
# Item Image
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
# Chat
# =========================
class Chat(models.Model):
    STATUS_CHOICES = (
        ("OPEN", "Open"),
        ("CLOSED", "Closed"),
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="chats"
    )

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="buyer_chats"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="OPEN"
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
            raise ValidationError("You cannot chat with yourself.")

        # Only block chat creation, not existing chats
        if not self.pk and self.item.status != "ACTIVE":
            raise ValidationError("Cannot start chat on inactive item.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Chat for {self.item.title}"


# =========================
# Message
# =========================
class Message(models.Model):
    MESSAGE_TYPES = (
        ("TEXT", "Text"),
        ("SYSTEM", "System"),
    )

    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    message_type = models.CharField(
        max_length=10,
        choices=MESSAGE_TYPES,
        default="TEXT"
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
        if self.sender not in (self.chat.buyer, self.chat.seller):
            raise ValidationError("Sender must be part of the chat.")

        if self.chat.status != "OPEN":
            raise ValidationError("Chat is closed.")

        if self.message_type == "TEXT" and not self.text.strip():
            raise ValidationError("Message cannot be empty.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        # Update chat activity safely
        Chat.objects.filter(id=self.chat_id).update(
            last_message_at=self.created_at
        )

    def __str__(self):
        return f"Message from {self.sender.phone_number}"


# =========================
# Report Post
# =========================
class ReportPost(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    reason = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Report by {self.user} on {self.item}"


# =========================
# Feedback
# =========================
class Feedback(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    feedback = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Feedback by {self.user}"
