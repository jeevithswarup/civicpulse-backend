from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES=(
        ('citizen','Citizens'),
        ('officer','Officer'),
        ('Admin','Admin'),
    )
    role=models.CharField(max_length=10,choices=ROLE_CHOICES,default='citizen')    
    phone=models.CharField(max_length=15,blank=True,null=True)
    profile_image = models.ImageField(upload_to="profiles/",blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username
    
    



