# scans/seed.py

from .models import XRayScan
import os
from faker import Faker
import random
import cloudinary.uploader
import datetime
import cloudinary
import os

# ✅ Explicitly configure Cloudinary (this is what was missing!)
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

def run():
    fake = Faker()
    tags_pool = ['lung', 'infection', 'fracture', 'opacity', 'fluid', 'pneumonia', 'normal', 'consolidation']
    
    sample_images_dir = 'sample_xray_images'
    
    if not os.path.exists(sample_images_dir):
        print(f"❌ Please create '{sample_images_dir}' directory in your project root and add X-ray images")
        return
    
    image_files = [f for f in os.listdir(sample_images_dir) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    if not image_files:
        print(f"❌ No image files found in '{sample_images_dir}' directory")
        return

    print(f"📁 Found {len(image_files)} images: {image_files}")

    # Delete existing scans
    XRayScan.objects.all().delete()
    print("🗑️ Cleared existing scan data")

    for i in range(min(len(image_files) * 2, 15)):
        selected_image = random.choice(image_files)
        image_path = os.path.join(sample_images_dir, selected_image)
        
        body_parts = ['Chest', 'Knee', 'Arm', 'Hand', 'Spine', 'Hip', 'Shoulder']
        selected_body_part = random.choice(body_parts)
        
        diagnosis_map = {
            'Chest': ['Pneumonia', 'Normal', 'Pleural Effusion', 'Tuberculosis', 'Lung Nodule'],
            'Knee': ['Normal', 'Arthritis', 'Fracture', 'Torn Meniscus'],
            'Arm': ['Fracture', 'Normal', 'Dislocation'],
            'Hand': ['Fracture', 'Normal', 'Arthritis'],
            'Spine': ['Normal', 'Disc Herniation', 'Scoliosis', 'Fracture'],
            'Hip': ['Normal', 'Hip Dysplasia', 'Fracture', 'Arthritis'],
            'Shoulder': ['Normal', 'Dislocation', 'Rotator Cuff Tear', 'Fracture']
        }

        selected_diagnosis = random.choice(diagnosis_map.get(selected_body_part, ['Normal']))

        tag_map = {
            'Pneumonia': ['lung', 'infection', 'opacity', 'consolidation'],
            'Fracture': ['fracture', 'bone', 'break'],
            'Normal': ['normal', 'clear'],
            'Pleural Effusion': ['fluid', 'lung', 'pleural'],
            'Arthritis': ['joint', 'arthritis', 'inflammation']
        }

        relevant_tags = tag_map.get(selected_diagnosis, tags_pool)
        selected_tags = random.sample(relevant_tags, min(3, len(relevant_tags)))

        try:
            upload_result = cloudinary.uploader.upload(image_path)
            cloudinary_url = upload_result.get("secure_url")
            
            scan = XRayScan(
                patient_id=f"P{i+1:05d}",
                body_part=selected_body_part,
                scan_date=fake.date_between(start_date="-2y", end_date="today"),
                institution=random.choice([
                    'Mayo Clinic', 
                    'Johns Hopkins', 
                    'Stanford Medical', 
                    'Cleveland Clinic',
                    'Mass General Hospital'
                ]),
                description=fake.sentence(nb_words=10),
                diagnosis=selected_diagnosis,
                tags=selected_tags,
                image=cloudinary_url
            )
            scan.save()
            print(f"✅ Created scan {i+1}: {scan.patient_id} - {selected_body_part} - {selected_diagnosis}")
        
        except Exception as e:
            print(f"❌ Error creating scan {i+1}: {e}")
            continue

    print(f"\n🎉 Successfully created {XRayScan.objects.count()} X-ray scans with Cloudinary images!")
