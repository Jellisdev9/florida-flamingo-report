from django.db import models
from articles.models import Article


class NotableSale(models.Model):
    class Region(models.TextChoices):
        SOUTH_FLORIDA = "SOUTH_FLORIDA", "South Florida"
        TAMPA_BAY = "TAMPA_BAY", "Tampa Bay"
        ORLANDO = "ORLANDO", "Orlando"
        JACKSONVILLE = "JACKSONVILLE", "Jacksonville"
        PANHANDLE = "PANHANDLE", "Panhandle"

    class PropertyType(models.TextChoices):
        WATERFRONT_ESTATE = "WATERFRONT_ESTATE", "Waterfront Estate"
        CONDO_PENTHOUSE = "CONDO_PENTHOUSE", "Condo Penthouse"
        CONDO_RESIDENCE = "CONDO_RESIDENCE", "Condo Residence"
        COMMERCIAL = "COMMERCIAL", "Commercial"
        SINGLE_FAMILY = "SINGLE_FAMILY", "Single Family"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PENDING_REVIEW = "PENDING_REVIEW", "Pending Review"
        PUBLISHED = "PUBLISHED", "Published"

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    location = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=20, choices=Region.choices)
    property_type = models.CharField(max_length=20, choices=PropertyType.choices)
    close_date = models.DateField()
    hero_image_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    article = models.OneToOneField(
        Article, null=True, blank=True, on_delete=models.SET_NULL, related_name="sale"
    )
    brokerage = models.CharField(max_length=255, blank=True)
    beds = models.PositiveSmallIntegerField(null=True, blank=True)
    baths = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    sq_ft = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PUBLISHED
    )
    # Attribution for auto-generated/scraped sale records — blank for
    # hand-entered ones.
    source_url = models.URLField(blank=True)
    source_name = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-close_date", "-price"]

    @property
    def price_display(self):
        # Formats price as "$4,750,000" — used by templates (no DB column needed)
        return f"${self.price:,.0f}"

    def __str__(self):
        return f"{self.title} — ${self.price:,.0f}"
