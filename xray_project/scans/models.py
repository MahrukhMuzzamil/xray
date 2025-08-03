from django.db import models
from cloudinary.models import CloudinaryField

class XRayScan(models.Model):
    patient_id = models.CharField(max_length=50)
    image = CloudinaryField('image', blank=True, null=True)
    body_part = models.CharField(max_length=100)
    scan_date = models.DateField()
    institution = models.CharField(max_length=255)
    description = models.TextField()
    diagnosis = models.CharField(max_length=255)
    tags = models.JSONField(default=list)  # Store as list of strings

    def __str__(self):
        return f"{self.patient_id} - {self.body_part}"
