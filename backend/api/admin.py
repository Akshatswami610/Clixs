from django.contrib import admin
from .models import Item, ItemImage, ReportPost, ContactForm

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'item_type', 'created_at')
    search_fields = ('title',)

admin.site.register(ItemImage)
admin.site.register(ContactForm)
admin.site.register(ReportPost)

