from django.db import models
from users.models import CustomUser
# Create your models here.


class FamilyMembers(models.Model):
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
    profile_picture = models.ImageField(upload_to='family_profile_pics/', null=True, blank=True)
    relationship_status = models.CharField(
        max_length=10,
        choices=RELATIONSHIP_STATUS_CHOICES,
        default='single',
    )
    added_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='family_members')

    def __str__(self):
        return self.full_name