from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    profile_pic = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
