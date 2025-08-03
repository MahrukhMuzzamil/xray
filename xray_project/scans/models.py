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

    def save(self, *args, **kwargs):
        # Ensure image URL is properly formatted before saving
        if self.image and not str(self.image).startswith('http'):
            # If it's a relative path, it should be handled by CloudinaryField
            # But let's ensure it's properly formatted
            pass
        super().save(*args, **kwargs)