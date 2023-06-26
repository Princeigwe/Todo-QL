from django.db import models

# Create your models here.

class Todo(models.Model):
    CATEGORY_CHOICES = (
        ("IMPORTANT", "Important"),
        ("URGENT", "Urgent"),
        ("DEFAULT", "Default")
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    
    def __str__(self): 
        return self.name