from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    student_id = models.CharField(max_length=50, blank=True, help_text="Student ID number")
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    # image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    image = models.ImageField(upload_to='profile_images', default='profile_images/default.png', blank=True)
    def __str__(self):
        return f'{self.user.username} Profile'