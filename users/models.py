from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    # Extend later with profile fields (phone, address, image)
    phone = models.CharField(max_length=20, blank=True)
    def __str__(self):
        return self.username

class OTPCode(models.Model):
    """One-time code for OTP authentication. 
    Stores the code (plaintext for demo) and expiry. In production, consider hashing the code.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps', null=True, blank=True)
    email = models.EmailField()  # email the code was requested for (may be used to create a user)
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['expires_at']),
        ]

    def is_expired(self):
        return timezone.now() > self.expires_at

    @classmethod
    def create_for_email(cls, email, code, lifetime_minutes=10, user=None):
        return cls.objects.create(
            user=user,
            email=email,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=lifetime_minutes)
        )

class Notification(models.Model):
    """Simple Notification model to store messages for users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.user_id}: {self.title[:20]}"
