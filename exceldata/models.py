from django.db import models

# Create your models here.
class DataImport(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    date_created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.first_name
    