from django.contrib import admin
from .models import Item, Category

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'category', 'posted_by',
                    'date_reported', 'is_resolved']
    list_filter = ['status', 'is_resolved', 'category']
    search_fields = ['title', 'description', 'location']
    list_editable = ['is_resolved']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass