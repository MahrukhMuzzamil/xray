from django.core.management.base import BaseCommand
from scans.models import XRayScan
from django.core.files import File
import os
from faker import Faker
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Seed the database with sample X-ray scans'

    def handle(self, *args, **options):
        fake = Faker()
        tags_pool = ['lung', 'infection', 'fracture', 'opacity', 'fluid', 'normal', 'abnormal', 'scan', 'x-ray']
        
        # Use the sample.jpg file that exists in the media directory
        image_path = 'media/sample.jpg'
        
        if not os.path.exists(image_path):
            self.stdout.write(
                self.style.ERROR(f'Image file {image_path} does not exist')
            )
            return
            
        for i in range(10):
            # Create a unique file name for each scan
            file_name = f"xray_{i}.jpg"
            
            with open(image_path, 'rb') as f:
                scan = XRayScan(
                    patient_id=f"P{i:05}",
                    body_part=random.choice(['Chest', 'Knee', 'Arm', 'Head', 'Spine']),
                    scan_date=fake.date_between(start_date="-2y", end_date="today"),
                    institution=random.choice(['Mayo Clinic', 'Johns Hopkins', 'Stanford', 'Cleveland Clinic', 'UCLA Medical Center']),
                    description=fake.sentence(),
                    diagnosis=random.choice(['Pneumonia', 'Fracture', 'Normal', 'Infection', 'Tumor']),
                    tags=random.sample(tags_pool, random.randint(2, 5))
                )
                # Save the image file
                scan.image.save(file_name, File(f), save=True)
                
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created scan {scan.patient_id}')
            )