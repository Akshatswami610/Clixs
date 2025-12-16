from django.contrib import admin
from .models import Item, ItemImage, ReportPost, ContactForm, CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'first_name', 'last_name', 'date_joined', 'is_active')
    search_fields = ('phone_number', 'first_name', 'last_name')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'item_type', 'created_at')
    search_fields = ('title',)

admin.site.register(ItemImage)
admin.site.register(ContactForm)
admin.site.register(ReportPost)

