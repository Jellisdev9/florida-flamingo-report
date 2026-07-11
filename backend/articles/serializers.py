from rest_framework import serializers
from .models import Article


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "slug", "headline", "subheadline", "category",
            "byline", "read_time_minutes", "hero_image_url",
            "published_date", "is_featured",
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    sale_facts = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = "__all__"

    def get_sale_facts(self, obj):
        try:
            sale = obj.sale
            return {
                "price_display": f"${sale.price:,.0f}",
                "location": sale.location,
                "brokerage": sale.brokerage,
                "beds": sale.beds,
                "baths": float(sale.baths) if sale.baths else None,
                "sq_ft": sale.sq_ft,
            }
        except Exception:
            return None
