from django.db import models

class XRayScan(models.Model):
    patient_id = models.CharField(max_length=50)
    image = models.ImageField(upload_to='xray_images/')
    body_part = models.CharField(max_length=100)
    scan_date = models.DateField()
    institution = models.CharField(max_length=255)
    description = models.TextField()
    diagnosis = models.CharField(max_length=255)
    tags = models.JSONField()  # Store as list of strings

    def __str__(self):
        return f"{self.patient_id} - {self.body_part}"
