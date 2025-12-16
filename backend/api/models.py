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
        user.set_password(password)  # 🔐 HASHED
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(phone_number, password, **extra_fields)


# =========================
# Custom User Model
# =========================
class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)

    email = models.EmailField(blank=True, null=True)
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

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]


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
                raise ValidationError("Sell price is required for SELL items.")
            if self.rent_prices:
                raise ValidationError("Rent prices are not allowed for SELL items.")

        if self.item_type == "RENT":
            if not self.rent_prices:
                raise ValidationError("Rent pricing is required for RENT items.")
            if not isinstance(self.rent_prices, dict):
                raise ValidationError("Rent prices must be a dictionary.")
            for value in self.rent_prices.values():
                if not isinstance(value, (int, float)):
                    raise ValidationError("Rent prices must be numbers.")

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

    def __str__(self):
        return f"Image for {self.item.title}"


# =========================
# Contact Form
# =========================
class ContactForm(models.Model):
    STATUS = (
        ("PENDING", "Pending"),
        ("RESOLVED", "Resolved"),
    )
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=50)
    message = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default="PENDING"
    )
    created_at = models.DateTimeField(default=timezone.now)

    def clean(self):
        if not self.email and not self.phone:
            raise ValidationError("Provide either email or phone.")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Contact Forms"


# =========================
# Report Post
# =========================
class ReportPost(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
