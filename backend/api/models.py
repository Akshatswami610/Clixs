from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import User

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """Create and save a user with a phone number only."""
        if not phone_number:
            raise ValueError("The phone number field must be set.")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """Create and save a SuperUser with a phone number."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number=phone_number, password=password, **extra_fields)


# -----------------------
# Custom User Model
# -----------------------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=False, null=True, blank=True)  # only for updates, not login
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']


from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Item(models.Model):
    ITEM_TYPES = (
        ('SELL', 'Sell'),
        ('RENT', 'Rent'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    item_type = models.CharField(max_length=5, choices=ITEM_TYPES)

    # Used only if SELL
    sell_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    rent_prices = models.JSONField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.item_type == 'SELL' and not self.sell_price:
            raise ValidationError("Sell price is required for SELL items.")

        if self.item_type == 'RENT' and not self.rent_prices:
            raise ValidationError("Rent prices are required for RENT items.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='clixs/images')

    def __str__(self):
        return f"Image for {self.item.title}"


class ContactForm(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Contact Forms"

class ReportPost(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)