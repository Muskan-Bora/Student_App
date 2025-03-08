from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, default="Full Name")
    roll_no = models.CharField(max_length=50, default="Roll No")
    std = models.CharField(max_length=20, default="std")
    division = models.CharField(max_length=10, default="A")
    image = models.ImageField(default='profilepic.png', upload_to='profile_pictures')

    def __str__(self):
        return f"{self.user.username}'s Profile"