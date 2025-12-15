from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Employee(models.Model):
    emp_id=models.CharField(max_length=20)
    emp_name=models.CharField(max_length=50)
    designation=models.CharField(max_length=50)
    
    def __str__(self):
        return self.emp_name