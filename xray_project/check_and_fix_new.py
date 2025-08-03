import os
import django
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xray_project.settings')
django.setup()

from scans.models import XRayScan

def check_and_fix_new():
    """Check current data and fix only new uploads"""
    scans = XRayScan.objects.all()
    print(f"📊 Found {scans.count()} scans")
    
    # Check environment variables
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    print(f"Cloudinary Cloud Name: {cloud_name}")
    
    print("\n📋 Current scan data:")
    for i, scan in enumerate(scans[:5]):  # Show first 5 scans
        print(f"\nScan {i+1}:")
        print(f"  ID: {scan.id}")
        print(f"  Patient ID: {scan.patient_id}")
        print(f"  Body Part: {scan.body_part}")
        print(f"  Image URL: {scan.image}")
        
        if scan.image:
            image_url = str(scan.image)
            if image_url.startswith('http'):
                print(f"  ✅ Full URL")
            elif image_url.startswith('image/upload/'):
                print(f"  ⚠️ Relative path - needs fixing")
                # Fix only if it's a relative path
                if cloud_name:
                    fixed_url = f"https://res.cloudinary.com/{cloud_name}/{image_url}"
                    print(f"  Fixed URL: {fixed_url}")
                    scan.image = fixed_url
                    scan.save()
                    print(f"  ✅ Fixed!")
                else:
                    print(f"  ❌ No cloud name available")
            else:
                print(f"  ⚠️ Unknown format")
    
    # Test API
    print("\n🧪 Testing API...")
    base_url = "https://xray-backend-391z.onrender.com/api"
    
    try:
        response = requests.get(f"{base_url}/scans/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API returned {len(data)} scans")
            
            if data:
                print("\n📋 API sample data:")
                for i, scan in enumerate(data[:3]):
                    image_url = scan.get('image', 'No image')
                    print(f"  Scan {i+1}: {image_url}")
        else:
            print(f"❌ API error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ API test failed: {e}")

if __name__ == "__main__":
    check_and_fix_new() 