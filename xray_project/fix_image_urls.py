import os
import django
import re

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xray_project.settings')
django.setup()

from scans.models import XRayScan

def fix_image_urls():
    """Fix malformed Cloudinary URLs in the database"""
    scans = XRayScan.objects.all()
    print(f"📊 Found {scans.count()} scans to check")
    
    fixed_count = 0
    
    for scan in scans:
        if scan.image:
            image_url = str(scan.image)
            print(f"\n🔍 Checking scan {scan.id}: {scan.patient_id}")
            print(f"   Original URL: {image_url}")
            
            # Check if URL has the duplicate image/upload/ issue
            if 'image/upload/https://' in image_url:
                # Fix the malformed URL
                fixed_url = image_url.replace('image/upload/https://', 'https://')
                print(f"   Fixed URL: {fixed_url}")
                
                # Update the scan
                scan.image = fixed_url
                scan.save()
                fixed_count += 1
                print(f"   ✅ Fixed!")
            elif 'image/upload/http://' in image_url:
                # Fix the malformed URL
                fixed_url = image_url.replace('image/upload/http://', 'http://')
                print(f"   Fixed URL: {fixed_url}")
                
                # Update the scan
                scan.image = fixed_url
                scan.save()
                fixed_count += 1
                print(f"   ✅ Fixed!")
            else:
                print(f"   ✅ URL looks correct")
    
    print(f"\n🎉 Fixed {fixed_count} malformed image URLs!")

if __name__ == "__main__":
    fix_image_urls() 