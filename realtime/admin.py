from django.contrib import admin
from .models import ShoppingSession, SessionMessage, SharedProduct

@admin.register(ShoppingSession)
class ShoppingSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'host', 'session_name', 'is_active', 'created_at', 'total_participants')
    list_filter = ('is_active', 'created_at')
    search_fields = ('session_id', 'host__email', 'session_name')
    readonly_fields = ('session_id', 'created_at', 'updated_at')
    filter_horizontal = ('participants',)

@admin.register(SessionMessage)
class SessionMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'user', 'message_type', 'timestamp')
    list_filter = ('message_type', 'timestamp')
    search_fields = ('user__email', 'message')
    readonly_fields = ('timestamp',)

@admin.register(SharedProduct)
class SharedProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'user', 'session', 'product_price', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('product_name', 'user__email')
    readonly_fields = ('timestamp',)