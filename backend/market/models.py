from django.db import models


class MarketMetric(models.Model):
    city = models.CharField(max_length=100)
    metric_label = models.CharField(max_length=100)
    value_display = models.CharField(max_length=50)
    change_display = models.CharField(max_length=20)
    is_positive = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    # Attribution for auto-generated/scraped data — blank for hand-entered.
    source_url = models.URLField(blank=True)
    source_name = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.city} — {self.metric_label}"


class Agent(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    volume_display = models.CharField(max_length=50)
    rank = models.PositiveSmallIntegerField()
    period_month = models.PositiveSmallIntegerField()
    period_year = models.PositiveSmallIntegerField()
    source_url = models.URLField(blank=True)
    source_name = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["rank"]
        unique_together = [["rank", "period_month", "period_year"]]

    def __str__(self):
        return f"#{self.rank} {self.name}"


class NeighborhoodIntel(models.Model):
    class Tag(models.TextChoices):
        HOT = "HOT", "Hot"
        RISING = "RISING", "Rising"
        COOLING = "COOLING", "Cooling"
        STABLE = "STABLE", "Stable"

    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField()
    tag = models.CharField(max_length=10, choices=Tag.choices)
    sort_order = models.PositiveSmallIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    source_url = models.URLField(blank=True)
    source_name = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.neighborhood} ({self.tag})"


class FastestGrowingMarket(models.Model):
    location = models.CharField(max_length=100)
    change_display = models.CharField(max_length=20)
    rank = models.PositiveSmallIntegerField()
    period_month = models.PositiveSmallIntegerField()
    period_year = models.PositiveSmallIntegerField()
    source_url = models.URLField(blank=True)
    source_name = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["rank"]
        unique_together = [["rank", "period_month", "period_year"]]

    def __str__(self):
        return f"#{self.rank} {self.location} — {self.change_display}"
