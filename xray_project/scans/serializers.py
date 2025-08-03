from rest_framework import serializers
from .models import XRayScan
import json
import os

class XRayScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = XRayScan
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Ensure tags is a list
        if isinstance(representation.get('tags'), str):
            try:
                representation['tags'] = json.loads(representation['tags'])
            except json.JSONDecodeError:
                representation['tags'] = []
        elif representation.get('tags') is None:
            representation['tags'] = []
        
        # Handle image URL - only fix if it's a relative path
        if representation.get('image'):
            image_url = str(representation['image'])
            
            # Only fix if it's a relative path starting with image/upload/
            if image_url.startswith('image/upload/') and not image_url.startswith('http'):
                # This is a relative path, construct full URL
                cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME', 'drgsmg6aq')
                representation['image'] = f"https://res.cloudinary.com/{cloud_name}/{image_url}"
            else:
                # Keep the URL as is for existing data
                representation['image'] = image_url
        
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
            # Check if it's an image file
            if hasattr(value, 'content_type'):
                if not value.content_type.startswith('image/'):
                    raise serializers.ValidationError("File must be an image.")
            
            # Check file size (limit to 10MB)
            if hasattr(value, 'size') and value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("Image file size must be less than 10MB.")
        
        return value
