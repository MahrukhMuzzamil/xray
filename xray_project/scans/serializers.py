from rest_framework import serializers
from .models import XRayScan
import json
import cloudinary.utils

class XRayScanSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = XRayScan
        fields = '__all__'

    def get_image_url(self, obj):
        """Get the proper Cloudinary URL"""
        if obj.image:
            try:
                # Use Cloudinary's built-in URL generation
                url = cloudinary.utils.cloudinary_url(str(obj.image))[0]
                print(f"🔗 Generated Cloudinary URL for {obj.patient_id}: {url}")
                return url
            except Exception as e:
                print(f"❌ Error generating Cloudinary URL for {obj.patient_id}: {e}")
                return str(obj.image)
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Handle tags field
        if isinstance(representation.get('tags'), str):
            try:
                representation['tags'] = json.loads(representation['tags'])
            except json.JSONDecodeError:
                representation['tags'] = []
        elif representation.get('tags') is None:
            representation['tags'] = []
        
        # Use the proper image URL
        representation['image'] = self.get_image_url(instance)
        
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
            # Check content type if available
            if hasattr(value, 'content_type'):
                if not value.content_type.startswith('image/'):
                    raise serializers.ValidationError("File must be an image.")
            
            # Check file size if available
            if hasattr(value, 'size') and value.size > 10 * 1024 * 1024:
                raise serializers.ValidationError("Image file size must be less than 10MB.")
        
        return value