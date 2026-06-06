from rest_framework import serializers

from .models import URLMapping


class URLMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLMapping
        fields = ["original_url", "short_url", "click_count", "created_at", "expired_at"]
        read_only_fields = ["id", "short_url", "created_at"]

    def validate_original_url(self, value):
        if not value.startswith("http://") and not value.startswith("https://"):
            raise serializers.ValidationError("Url must start with http:// or https://")
        return value

    def validate_expired_at(self, value):
        if value and value <= self.context["request"].data.get("created_at"):
            raise serializers.ValidationError("Expiration date must be in the future")
        return value
