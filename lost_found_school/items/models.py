from django.db import models
from django.contrib.auth.models import User
 
 
class UserProfile(models.Model):
    user           = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role           = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
 
    def __str__(self):
        return f"{self.user.username} — {self.role or 'No role'}"
 
 
class Category(models.Model):
    name = models.CharField(max_length=100)
 
    def __str__(self):
        return self.name
 
    class Meta:
        verbose_name_plural = "Categories"
 
 
class Item(models.Model):
    STATUS_CHOICES = [
        ('lost',  'Lost'),
        ('found', 'Found'),
    ]
 
    title          = models.CharField(max_length=200)
    description    = models.TextField()
    status         = models.CharField(max_length=5, choices=STATUS_CHOICES)
    category       = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    location       = models.CharField(max_length=200)
    date_reported  = models.DateTimeField(auto_now_add=True)
    date_lost_found = models.DateField()
    photo          = models.ImageField(upload_to='item_photos/', blank=True, null=True)
    posted_by      = models.ForeignKey(User, on_delete=models.CASCADE)
    is_resolved    = models.BooleanField(default=False)
 
    def __str__(self):
        return f"[{self.status.upper()}] {self.title}"
 
    class Meta:
        ordering = ['-date_reported']