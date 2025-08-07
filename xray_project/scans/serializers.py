from rest_framework import serializers
from .models import XRayScan
import json
import re
import os

class XRayScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = XRayScan
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        
        if isinstance(representation.get('tags'), str):
            try:
                representation['tags'] = json.loads(representation['tags'])
            except json.JSONDecodeError:
                representation['tags'] = []
        elif representation.get('tags') is None:
            representation['tags'] = []
        
        
        if representation.get('image'):
            image_url = str(representation['image'])
            
            # Get cloud name from environment or use default
            cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME', 'drgsmg6aq')
            
            # Check if it's a partial Cloudinary path that needs fixing
            if image_url.startswith('image/upload/'):
                # This is a relative path, make it a full Cloudinary URL
                fixed_url = f"https://res.cloudinary.com/{cloud_name}/{image_url}"
                representation['image'] = fixed_url
                print(f"🔧 Fixed image URL: {image_url} -> {fixed_url}")
                
            elif 'image/upload/https://' in image_url:
                # Fix double URL issue
                fixed_url = image_url.replace('image/upload/https://', 'https://')
                representation['image'] = fixed_url
                print(f"🔧 Fixed malformed URL: {image_url} -> {fixed_url}")
                
            elif 'image/upload/http://' in image_url:
                # Fix double URL issue
                fixed_url = image_url.replace('image/upload/http://', 'http://')
                representation['image'] = fixed_url
                print(f"🔧 Fixed malformed URL: {image_url} -> {fixed_url}")
                
            elif not image_url.startswith('http') and '/' in image_url:
                # Handle cases where we have a path but no domain
                if image_url.startswith('/'):
                    image_url = image_url[1:]  # Remove leading slash
                
                # Check if it looks like a Cloudinary path
                if 'v' in image_url and ('.' in image_url.split('/')[-1]):
                    fixed_url = f"https://res.cloudinary.com/{cloud_name}/image/upload/{image_url}"
                    representation['image'] = fixed_url
                    print(f"🔧 Fixed relative URL: {image_url} -> {fixed_url}")
            
            # If it's already a proper HTTP URL, leave it as is
            elif image_url.startswith('http'):
                print(f"✅ URL already correct: {image_url}")
            else:
                print(f"⚠️ Unknown URL format: {image_url}")
        
        return representation

    def validate_tags(self, value):
        """
        Ensure the tags field is a valid list, even if passed as a stringified JSON.
        """
        if isinstance(value, list):
            return value

        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                pass

        raise serializers.ValidationError("Value must be valid JSON list.")

    def validate_image(self, value):
        """
        Validate that the image file is provided and is an image.
        """
        if value:
            
            if hasattr(value, 'content_type'):
                if not value.content_type.startswith('image/'):
                    raise serializers.ValidationError("File must be an image.")
            
            
            if hasattr(value, 'size') and value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("Image file size must be less than 10MB.")
        
        return value
