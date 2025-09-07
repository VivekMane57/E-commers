import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class ShoppingSession(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_shopping_sessions')
    participants = models.ManyToManyField(User, blank=True, related_name='joined_shopping_sessions')
    session_name = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Session {self.session_id} by {self.host.email}"
    
    @property
    def total_participants(self):
        return self.participants.count() + 1  # +1 for host

class SessionMessage(models.Model):
    """Messages sent during shopping sessions"""
    session = models.ForeignKey(ShoppingSession, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    message_type = models.CharField(max_length=50, default='chat')  # chat, product_share, system
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.user.email}: {self.message[:50]}..."

class SharedProduct(models.Model):
    """Products shared during shopping sessions"""
    session = models.ForeignKey(ShoppingSession, on_delete=models.CASCADE, related_name='shared_products')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_url = models.URLField(blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_image = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product_name} shared by {self.user.email}"