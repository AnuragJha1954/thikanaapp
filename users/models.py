from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    
    RELATIONSHIP_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('separated', 'Separated'),
    ]
    
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    thikana = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    education = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    isVerified = models.BooleanField(default=False)
    isRejected = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    relationship_status = models.CharField(
        max_length=10,
        choices=RELATIONSHIP_STATUS_CHOICES,
        default='single',
    )

    def __str__(self):
        return f"Memeber named {self.full_name} born on {self.date_of_birth} from {self.thikana}"
