from django.db import models



class Department(models.Model):

    dept_id=models.CharField(max_length=17,unique=True)
    dept_name=models.CharField(max_length=100)
    descrption=models.TextField(blank=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.dept_name
    
    
    