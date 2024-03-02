from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=200, blank=False)
    location_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=100, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name