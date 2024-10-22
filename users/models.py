from django.db import models

# Create your models here.
class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    company_name = models.CharField(max_length=255)
    owner_first_name = models.CharField(max_length=100)
    owner_last_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return self.company_name