# scans/seed.py
from .models import XRayScan
from django.core.files import File
import os
from faker import Faker
import random
import datetime

def run():
    fake = Faker()
    tags_pool = ['lung', 'infection', 'fracture', 'opacity', 'fluid']

    for i in range(10):
        image_path = 'media/sample.jpg'  # Use any placeholder
        with open(image_path, 'rb') as f:
            scan = XRayScan(
                patient_id=f"P{i:05}",
                image=File(f, name=f"xray_{i}.jpg"),
                body_part=random.choice(['Chest', 'Knee', 'Arm']),
                scan_date=fake.date_between(start_date="-2y", end_date="today"),
                institution=random.choice(['Mayo Clinic', 'Johns Hopkins', 'Stanford']),
                description=fake.sentence(),
                diagnosis=random.choice(['Pneumonia', 'Fracture', 'Normal']),
                tags=random.sample(tags_pool, 3)
            )
            scan.save()
