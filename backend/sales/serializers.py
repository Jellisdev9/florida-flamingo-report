from rest_framework import serializers
from .models import NotableSale


class NotableSaleSerializer(serializers.ModelSerializer):
    price_display = serializers.SerializerMethodField()

    class Meta:
        model = NotableSale
        fields = "__all__"

    def get_price_display(self, obj):
        return f"${obj.price:,.0f}"


class NotableSaleListSerializer(serializers.ModelSerializer):
    price_display = serializers.SerializerMethodField()

    class Meta:
        model = NotableSale
        fields = [
            "slug", "title", "price", "price_display", "city", "region",
            "property_type", "close_date", "hero_image_url", "is_featured",
        ]

    def get_price_display(self, obj):
        return f"${obj.price:,.0f}"
