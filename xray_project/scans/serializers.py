from rest_framework import serializers
from .models import XRayScan
import json

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
        
        # Ensure image URL is properly formatted
        if representation.get('image'):
            # If it's a Cloudinary URL, ensure it's properly formatted
            image_url = str(representation['image'])
            if not image_url.startswith('http'):
                # If it's not a full URL, it might be a relative path
                # This shouldn't happen with Cloudinary, but just in case
                representation['image'] = image_url
            else:
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
