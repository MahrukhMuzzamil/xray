import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xray_project.settings')
django.setup()

def check_cloudinary_config():
    """Check Cloudinary configuration"""
    print("🔧 Checking Cloudinary configuration...")
    print("=" * 50)
    
    # Check environment variables
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    api_key = os.getenv('CLOUDINARY_API_KEY')
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
    
    print(f"Cloudinary Cloud Name: {'✅ Set' if cloud_name else '❌ Not set'}")
    print(f"Cloudinary API Key: {'✅ Set' if api_key else '❌ Not set'}")
    print(f"Cloudinary API Secret: {'✅ Set' if api_secret else '❌ Not set'}")
    
    if not all([cloud_name, api_key, api_secret]):
        print("\n❌ Cloudinary environment variables are not properly configured!")
        print("Please set the following environment variables:")
        print("- CLOUDINARY_CLOUD_NAME")
        print("- CLOUDINARY_API_KEY")
        print("- CLOUDINARY_API_SECRET")
        return False
    
    print("\n✅ All Cloudinary environment variables are set!")
    
    # Test Cloudinary connection
    try:
        import cloudinary
        import cloudinary.uploader
        
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        
        print("✅ Cloudinary configuration successful!")
        return True
        
    except Exception as e:
        print(f"❌ Cloudinary configuration failed: {e}")
        return False

if __name__ == "__main__":
    check_cloudinary_config() 