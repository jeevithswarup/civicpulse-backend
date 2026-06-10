from django.db import models
from users.models import User


class Complaint(models.Model):

    CATEGORY_CHOICES=(
        ('road','road'),
        ('water','water'),
        ('electricity','electricity'),
        ('sanitation','sanitation'),
    )
    STATUS_CHOICES=(
        ('pending','pending'),
        ('assigned','assigned'),
        ('in_progress','in_progress'),
        ('resolved','resolved'),
        ('closed','closed'),
    )
    PRIORITY_CHOICES=(
        ('low','low'),
        ('medium','medium'),
        ('high','high'),
        ('emergency','emergency'),
    )

    complaintID=models.CharField(max_length=50,unique=True,blank=True)
    title=models.CharField(max_length=100)
    description=models.TextField()
    category=models.CharField(max_length=30,choices=CATEGORY_CHOICES,default='road')
    address=models.CharField(max_length=300)
    latitude=models.DecimalField(max_digits=10,decimal_places=7)
    longitude=models.DecimalField(max_digits=10,decimal_places=7)
    image=models.ImageField(upload_to='complaint_image/')
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    createdBy=models.ForeignKey(User,on_delete=models.CASCADE,related_name='complaint_created')
    priority=models.CharField(max_length=10,choices=PRIORITY_CHOICES,default='medium')
    assignedOfficer=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True,related_name='complaints_assigned')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)    
    def __str__(self):
        return self.title

