from django.db import models
from django.contrib.auth.models import AbstractUser
from departments.models import Department

class User(AbstractUser):
    ROLE_CHOICES=(
        ('citizen','Citizens'),
        ('worker','Worker'),
        ('officer','Officer'),
        ('admin','Admin'),
    )
    department=models.ForeignKey(Department,on_delete=models.SET_NULL,blank=True,null=True)
    role=models.CharField(max_length=10,choices=ROLE_CHOICES,default='citizen')   
    phone=models.CharField(max_length=15,blank=True,null=True,unique=True)
    preferred_language=models.CharField(max_length=20,default='English')
    profile_image = models.ImageField(upload_to="profiles/",blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.username} ({self.role})"
    

    
    



