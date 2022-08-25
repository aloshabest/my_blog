from django.db import models

class Contact(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.EmailField()
    Subject = models.CharField(max_length=100)
    Message = models.TextField()
    is_answered = models.BooleanField(default=False)
