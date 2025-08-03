import os
import django
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xray_project.settings')
django.setup()

from scans.models import XRayScan

def fix_image_urls_final():
    """Fix all image URLs to ensure they are full Cloudinary URLs"""
    scans = XRayScan.objects.all()
    print(f"📊 Found {scans.count()} scans to check")
    
    fixed_count = 0
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME', 'drgsmg6aq')  # Use your actual cloud name
    
    for scan in scans:
        if scan.image:
            image_url = str(scan.image)
            print(f"\n🔍 Checking scan {scan.id}: {scan.patient_id}")
            print(f"   Original URL: {image_url}")
            
            # Check if URL needs fixing
            if image_url.startswith('image/upload/'):
                # This is a relative path, need to make it full URL
                fixed_url = f"https://res.cloudinary.com/{cloud_name}/{image_url}"
                print(f"   Fixed URL: {fixed_url}")
                
                # Update the scan
                scan.image = fixed_url
                scan.save()
                fixed_count += 1
                print(f"   ✅ Fixed!")
            elif 'image/upload/https://' in image_url:
                # Fix malformed URL
                fixed_url = image_url.replace('image/upload/https://', 'https://')
                print(f"   Fixed URL: {fixed_url}")
                
                scan.image = fixed_url
                scan.save()
                fixed_count += 1
                print(f"   ✅ Fixed!")
            elif 'image/upload/http://' in image_url:
                # Fix malformed URL
                fixed_url = image_url.replace('image/upload/http://', 'http://')
                print(f"   Fixed URL: {fixed_url}")
                
                scan.image = fixed_url
                scan.save()
                fixed_count += 1
                print(f"   ✅ Fixed!")
            elif image_url.startswith('http'):
                print(f"   ✅ URL looks correct")
            else:
                print(f"   ⚠️ Unknown URL format: {image_url}")
    
    print(f"\n🎉 Fixed {fixed_count} image URLs!")
    
    # Test the API to verify fixes
    print("\n🧪 Testing API...")
    base_url = "https://xray-backend-391z.onrender.com/api"
    
    try:
        response = requests.get(f"{base_url}/scans/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API returned {len(data)} scans")
            
            if data:
                print("\n📋 Sample image URLs:")
                for i, scan in enumerate(data[:3]):
                    image_url = scan.get('image', 'No image')
                    print(f"   Scan {i+1}: {image_url}")
                    
                    if image_url and image_url.startswith('http'):
                        try:
                            img_response = requests.head(image_url, timeout=5)
                            print(f"   ✅ Image accessible: {img_response.status_code == 200}")
                        except Exception as e:
                            print(f"   ❌ Image not accessible: {e}")
        else:
            print(f"❌ API error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ API test failed: {e}")

if __name__ == "__main__":
    fix_image_urls_final() 