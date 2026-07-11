from django.db import models


class Article(models.Model):
    class Category(models.TextChoices):
        NOTABLE_SALE = "NOTABLE_SALE", "Notable Sale"
        AGENT_WATCH = "AGENT_WATCH", "Agent Watch"
        NEIGHBORHOOD_WATCH = "NEIGHBORHOOD_WATCH", "Neighborhood Watch"
        DEVELOPMENT = "DEVELOPMENT", "Development"
        MARKET_PULSE = "MARKET_PULSE", "Market Pulse"

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    headline = models.CharField(max_length=500)
    subheadline = models.CharField(max_length=500, blank=True)
    category = models.CharField(max_length=30, choices=Category.choices)
    body = models.TextField()
    byline = models.CharField(max_length=255)
    author_avatar_url = models.URLField(blank=True)
    read_time_minutes = models.PositiveSmallIntegerField(default=3)
    hero_image_url = models.URLField(blank=True)
    published_date = models.DateField()
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return self.headline
